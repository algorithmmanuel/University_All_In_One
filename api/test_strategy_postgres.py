"""Real bearer sessions and concurrent commands; disposable local PostgreSQL only."""
import os
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
import pytest


@pytest.mark.integration
def test_strategy_real_sessions_and_concurrent_commands():
    url = os.getenv('TEST_DATABASE_URL')
    if not url: pytest.skip('TEST_DATABASE_URL required')
    from sqlalchemy.engine import make_url
    p = make_url(url)
    if not (p.drivername.startswith('postgresql') and p.database == 'educyber_test' and p.host in ('localhost', '127.0.0.1')):
        pytest.fail('Refusing non-local or non-test database')
    if os.getenv('DATABASE_URL') != url: pytest.fail('Database URLs must match')
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, delete
    from sqlalchemy.orm import sessionmaker
    from database import Base
    from models import User, AuthSession
    from auth import issue_session
    import cyber_lab_routes as routes
    e = create_engine(url); Base.metadata.create_all(e); Session = sessionmaker(bind=e)
    ids = []; headers = []
    try:
        for role in ('student', 'student', 'teacher'):
            with Session() as db:
                user = User(full_name='Synthetic strategy learner', email=f'{uuid4().hex}@example.invalid', password_hash='disabled', role=role, is_active=True)
                db.add(user); db.flush(); ids.append(user.id)
                headers.append({'Authorization': 'Bearer ' + issue_session(db, user)})
        app = FastAPI(); app.include_router(routes.router)
        def get_db():
            with Session() as db: yield db
        app.dependency_overrides[routes.get_db] = get_db
        with TestClient(app) as client:
            assert client.get('/api/v1/cyber-lab/catalog').status_code == 401
            assert client.get('/api/v1/cyber-lab/catalog', headers=headers[2]).status_code == 403
            run = client.post('/api/v1/cyber-lab/runs', headers=headers[0]).json()
            endpoint = f"/api/v1/cyber-lab/runs/{run['id']}"
            assert client.get(endpoint, headers=headers[1]).status_code == 404
            def submit(body):
                with TestClient(app) as concurrent:
                    return concurrent.post(endpoint+'/commands', json=body, headers=headers[0])
            body = {'command_id': str(uuid4()), 'action': 'mfa', 'target': 'identity', 'expected_version': 0}
            with ThreadPoolExecutor(max_workers=2) as pool:
                responses = list(pool.map(submit, [body, body]))
            assert [r.status_code for r in responses] == [200, 200]
            saved = client.get(endpoint, headers=headers[0]).json()
            assert saved['version'] == 1 and saved['budget'] == 26 and saved['staff'] == 2
            bodies = [{'command_id': str(uuid4()), 'action': 'inspect', 'target': target, 'expected_version': 1} for target in ('app', 'staff')]
            with ThreadPoolExecutor(max_workers=2) as pool:
                responses = list(pool.map(submit, bodies))
            assert sorted(r.status_code for r in responses) == [200, 409]
            practice = client.post('/api/v1/cyber-lab/practice', json={'count': 5}, headers=headers[0]).json()
            assert client.get(f"/api/v1/cyber-lab/practice/{practice['id']}", headers=headers[1]).status_code == 404
            with Session.begin() as db: db.execute(delete(AuthSession).where(AuthSession.user_id == ids[0]))
            assert client.get(endpoint, headers=headers[0]).status_code == 401
    finally:
        with Session.begin() as db:
            db.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
            db.execute(delete(User).where(User.id.in_(ids)))
        e.dispose()
