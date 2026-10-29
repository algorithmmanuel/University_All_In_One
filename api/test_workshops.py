"""Authored cases, owned APIs and real-session PostgreSQL concurrency."""
from copy import deepcopy
from itertools import product
from uuid import uuid4
import pytest
from sqlalchemy import select
from journey_workshops import engine
from models import JourneyWorkshopRun
from test_red_blue_api import arena  # Shared real hashed-session/isolated DB fixture.


@pytest.mark.parametrize('case',list(engine.CASES.values()),ids=list(engine.CASES))
def test_every_case_supports_all_eight_paths_and_pinned_replay(case):
    for choices in product(('a','b'),repeat=3):
        s=engine.new_state(case);original=deepcopy(s)
        for i,choice in enumerate(choices):
            p=engine.project(s)
            assert set(p['step'])=={'prompt','context','choices'}
            assert all(set(c)=={'id','label','effort'} for c in p['step']['choices'])
            before=deepcopy(s)
            s=engine.advance(s,choice,i,f'command-{i}')
            assert before['decisions']==list(choices[:i])
            assert engine.advance(s,choice,i,f'command-{i}')==s
        p=engine.project(s)
        assert p['completed'] and len(p['recap'])==3 and p['step'] is None
        assert len(p['findings'])==choices.count('a')
        assert len(p['unresolved'])==choices.count('b')
        assert p['effort']==choices.count('a')*2+choices.count('b')
        assert original['decisions']==[] and case==s['snapshot']
        assert engine.summary(s)=={k:p[k] for k in ('findings','unresolved','effort')}


def test_workshop_owned_auth_stale_retry_and_comparison(arena):
    c,h,ids,Session,app,_=arena
    import workshop_routes as routes
    app.include_router(routes.router)
    catalog=c.get('/api/v1/workshops/catalog').json()
    assert len(catalog['cases'])==24 and all('steps' not in row for row in catalog['cases'])
    body={'case_id':'scholarship-pressure'}
    assert c.post('/api/v1/workshops/runs',json=body).status_code==401
    assert c.post('/api/v1/workshops/runs',json=body,headers=h[3]).status_code==403
    created=c.post('/api/v1/workshops/runs',json=body,headers=h[0]);assert created.status_code==201
    m=created.json();path=f"/api/v1/workshops/runs/{m['id']}"
    assert c.get(path,headers=h[1]).status_code==404
    assert c.get('/api/v1/workshops/runs',headers=h[1]).json()['runs']==[]
    assert c.post('/api/v1/workshops/runs',json={**body,'replay_of':m['id']},headers=h[0]).status_code==409
    first={'command_id':str(uuid4()),'expected_step':0,'choice_id':'b'}
    result=c.post(path+'/decisions',json=first,headers=h[0]);assert result.status_code==200
    assert c.post(path+'/decisions',json=first,headers=h[0]).json()==result.json()
    assert c.post(path+'/decisions',json={**first,'choice_id':'a'},headers=h[0]).status_code==409
    assert c.post(path+'/decisions',json={**first,'command_id':str(uuid4())},headers=h[0]).status_code==409
    for i in (1,2):
        result=c.post(path+'/decisions',json={'command_id':str(uuid4()),'expected_step':i,'choice_id':'a'},headers=h[0])
        assert result.status_code==200
    done=result.json();assert done['completed'] and len(done['unresolved'])==1
    replay=c.post('/api/v1/workshops/runs',json={**body,'replay_of':m['id']},headers=h[0]).json()
    assert replay['step_index']==0 and replay['baseline']['effort']==done['effort']
    assert c.post('/api/v1/workshops/runs',json={**body,'replay_of':m['id']},headers=h[1]).status_code==404
    assert c.post(path+'/decisions',json={**first,'command_id':str(uuid4())},headers=h[0]).status_code==409
    with Session() as db:
        saved=db.get(JourneyWorkshopRun,m['id'])
        assert len(saved.state['receipts'])==3 and saved.state['snapshot']==engine.CASES[body['case_id']]
    assert 'snapshot' not in done and 'receipts' not in done
    assert created.headers['cache-control']=='no-store'


def test_workshop_forged_state_and_body_bounds(arena):
    c,h,_,_,app,_=arena
    import workshop_routes as routes
    app.include_router(routes.router)
    for body in ({'case_id':'unknown'},{'case_id':'scholarship-pressure','findings':99},{'case_id':'../private'}):
        assert c.post('/api/v1/workshops/runs',headers=h[0],json=body).status_code==422
    assert c.post('/api/v1/workshops/runs',headers={**h[0],'Content-Type':'application/json'},content='x'*4097).status_code==413


def test_workshop_postgres_concurrency_and_rollback(arena):
    c,h,_,Session,app,dialect=arena
    if dialect!='postgres':pytest.skip('PostgreSQL row locks required')
    import workshop_routes as routes
    app.include_router(routes.router)
    from concurrent.futures import ThreadPoolExecutor
    from fastapi.testclient import TestClient
    from threading import Barrier
    m=c.post('/api/v1/workshops/runs',json={'case_id':'clinical-containment'},headers=h[0]).json()
    path=f"/api/v1/workshops/runs/{m['id']}"
    same={'command_id':str(uuid4()),'expected_step':0,'choice_id':'a'}
    def race(bodies):
        barrier=Barrier(2)
        def send(body):
            with TestClient(app) as client:
                barrier.wait(timeout=10)
                return client.post(path+'/decisions',json=body,headers=h[0])
        with ThreadPoolExecutor(max_workers=2) as pool:return list(pool.map(send,bodies))
    assert [r.status_code for r in race([same,same])]==[200,200]
    assert c.get(path,headers=h[0]).json()['effort']==2
    commands=[{'command_id':str(uuid4()),'expected_step':1,'choice_id':choice} for choice in ('a','b')]
    assert sorted(r.status_code for r in race(commands))==[200,409]
    from sqlalchemy import event
    from sqlalchemy.exc import OperationalError
    def failed(*_):raise OperationalError('synthetic update',{'private':'sentinel'},Exception('synthetic failure'))
    event.listen(JourneyWorkshopRun,'after_update',failed)
    final={'command_id':str(uuid4()),'expected_step':2,'choice_id':'a'}
    try:assert c.post(path+'/decisions',json=final,headers=h[0]).status_code==503
    finally:event.remove(JourneyWorkshopRun,'after_update',failed)
    assert c.get(path,headers=h[0]).json()['step_index']==2
    assert c.post(path+'/decisions',json=final,headers=h[0]).json()['completed']


def test_workshop_additive_migration_preserves_existing_records():
    import importlib.util
    from pathlib import Path
    from sqlalchemy import create_engine,text,inspect
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    spec=importlib.util.spec_from_file_location('workshop_migration',Path(__file__).parent/'migrations/versions/0013_journey_workshops.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    e=create_engine('sqlite://')
    with e.begin() as conn:
        conn.execute(text('CREATE TABLE users(id INTEGER PRIMARY KEY)'))
        conn.execute(text('CREATE TABLE red_blue_matches(id INTEGER PRIMARY KEY, transcript TEXT)'))
        conn.execute(text("INSERT INTO red_blue_matches VALUES(1,'retained-private-replay')"))
        with Operations.context(MigrationContext.configure(conn)):m.upgrade()
        assert 'journey_workshop_runs' in inspect(conn).get_table_names()
        with Operations.context(MigrationContext.configure(conn)):m.downgrade()
        assert conn.execute(text('SELECT * FROM red_blue_matches')).all()==[(1,'retained-private-replay')]
    e.dispose()
