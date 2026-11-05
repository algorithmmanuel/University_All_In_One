"""Build C coverage, frozen history and server-derived campaign evidence."""
import hashlib
import json
from collections import Counter
from copy import deepcopy
import pytest
from cyber_content import BANK, TOPICS, REVISION, lessons
from cyber_curriculum_v3 import app_source
from test_cyber_lab import lab_client
from test_build_b import supplier_win, answer


def test_build_b_250_question_objects_remain_exactly_frozen():
    assert hashlib.sha256(json.dumps(BANK[:250], sort_keys=True).encode()).hexdigest() == '6a97d479cfc4014ec9a9f82addb687d20ed14eb4300e2e4c2bd3dcf69681eb46'


def test_500_question_blueprint_and_teaching_alignment():
    assert len(BANK) == len({q['id'] for q in BANK}) == 500
    assert len({q['prompt'].strip().casefold() for q in BANK}) == 500
    for topic in TOPICS:
        questions = [q for q in BANK if q['topic'] == topic]
        assert Counter(q['difficulty'] for q in questions) == {'foundational': 20, 'applied': 20, 'challenging': 10}
        section = next(s for m in lessons() for s in m['sections'] if s['id'] == topic)
        assert len(section['worked_cases']) == 50 and len(section['steps']) == 3
        check = section['check']
        assert 0 <= check['answer'] < len(set(check['options'])) == 3
        for q in questions:
            assert len(set(q['options'])) == 3 and all(option.strip() for option in q['options'])
            assert q['explanation'] and q['source']['url'].startswith('https://')
            assert any(c['objective'] == q['objective'] and c['situation'] == q['prompt'] for c in section['worked_cases'])
    assert Counter(q['answer'] for q in BANK if q['revision'] == REVISION) == {0: 80, 1: 90, 2: 80}
    assert app_source(46)['title'] == 'OWASP: Deserialization'
    assert app_source(47)['title'] == 'OWASP: Content Security Policy'
    assert app_source(50)['title'] == 'OWASP: File Upload'


def test_catalog_and_campaign_do_not_reveal_practice_keys_or_hidden_game_state(lab_client):
    client, _, _ = lab_client
    catalog = client.get('/api/v1/cyber-lab/catalog').json()
    assert catalog['question_count'] == 500 and catalog['campaign']['completed'] == 0
    assert all(not c['module_read'] and c['wins'] == c['practice_distinct'] == 0 for c in catalog['campaign']['chapters'])
    practice = client.post('/api/v1/cyber-lab/practice', json={'topic': 'application', 'difficulty': 'foundational', 'count': 20}).json()
    assert len(practice['questions']) == 20
    assert all('answer' not in q and 'explanation' not in q for q in practice['questions'])
    # Formative lesson checks are intentionally visible, but cannot award credit.
    assert client.post('/api/v1/cyber-lab/campaign', json={'completed': 3}).status_code == 404
    chapter = client.get('/api/v1/cyber-lab/catalog').json()['campaign']['chapters'][1]
    assert chapter['practice_distinct'] == 0


def test_campaign_milestones_derive_from_owned_records_and_are_not_unlocks(lab_client):
    from models import StrategyRun
    client, Session, user = lab_client
    assert client.post('/api/v1/cyber-lab/study/defend/complete').status_code == 200
    for _ in range(2):
        session = client.post('/api/v1/cyber-lab/practice', json={'topic': 'network', 'count': 5}).json()
        assert answer(client, Session, session, False).status_code == 200
    with Session.begin() as db:
        db.add(StrategyRun(user_id=1, state=supplier_win('campaign')))
    chapter = client.get('/api/v1/cyber-lab/catalog').json()['campaign']['chapters'][1]
    assert chapter['module_read'] and chapter['wins'] == 1 and chapter['practice_distinct'] == 10
    assert chapter['milestones_met'] and chapter['next']['label'] == 'Compare another strategy'
    user.id = 2
    other = client.get('/api/v1/cyber-lab/catalog').json()['campaign']
    assert other['completed'] == 0 and all(c['practice_distinct'] == 0 and c['wins'] == 0 for c in other['chapters'])
    # Learning guidance must not gate scenario creation for a new learner.
    assert client.post('/api/v1/cyber-lab/runs', json={'scenario': 'ransomware'}).status_code == 201


def test_repeated_results_do_not_inflate_distinct_coverage(lab_client):
    from models import CyberPracticeSession
    client, Session, _ = lab_client
    q = deepcopy(BANK[0])
    with Session.begin() as db:
        for _ in range(6): db.add(CyberPracticeSession(user_id=1, snapshot=[q], result={
            'feedback': [{'id': q['id'], 'correct': True}]}))
    chapter = client.get('/api/v1/cyber-lab/catalog').json()['campaign']['chapters'][0]
    assert chapter['practice_distinct'] == 1 and not chapter['milestones_met']


def test_campaign_legacy_win_and_active_resume_survive_history_pagination(lab_client):
    import strategy_v1 as v1
    from models import StrategyRun
    client, Session, _ = lab_client
    legacy = v1.new_state('old'); legacy['status'] = 'won'
    assert 'scenario' not in legacy
    with Session.begin() as db:
        db.add(StrategyRun(user_id=1, state=legacy))
        active = StrategyRun(user_id=1, state=v1.new_state('active'));db.add(active);db.flush();active_id=active.id
        for _ in range(25): db.add(StrategyRun(user_id=1, state=supplier_win('pagination')))
    chapter = client.get('/api/v1/cyber-lab/catalog').json()['campaign']['chapters'][0]
    assert chapter['wins'] == 1 and chapter['resume_id'] == active_id
    assert len(client.get('/api/v1/cyber-lab/runs').json()['runs']) == 20


def test_prior_edition_read_and_old_practice_snapshot_are_preserved(lab_client, monkeypatch):
    from models import CyberStudyProgress, CyberPracticeSession
    import cyber_lab_routes as routes
    client, Session, _ = lab_client
    with Session.begin() as db:
        db.add(CyberStudyProgress(user_id=1, module_id='protect', revision='cyber-lab-v2'))
        saved = CyberPracticeSession(user_id=1, snapshot=deepcopy(BANK[:1]));db.add(saved);db.flush();saved_id=saved.id
    catalog = client.get('/api/v1/cyber-lab/catalog').json()
    assert catalog['modules'][0]['previously_completed'] and not catalog['modules'][0]['completed']
    assert not catalog['campaign']['chapters'][0]['module_read']
    monkeypatch.setattr(routes, 'BANK', [])
    assert answer(client, Session, {'id': saved_id}, True).json()['result']['score'] == 1
    assert client.get('/api/v1/cyber-lab/practice/'+str(saved_id)).json()['questions'][0]['revision'] == 'cyber-lab-v1'


@pytest.mark.parametrize('difficulty,count', [('foundational',20), ('applied',20), ('challenging',10)])
def test_new_topic_pools_and_snapshot_grading(lab_client, difficulty, count):
    client, Session, _ = lab_client
    started = client.post('/api/v1/cyber-lab/practice', json={'topic': 'application', 'difficulty': difficulty, 'count': count})
    assert started.status_code == 201
    assert len(started.json()['questions']) == count
    assert answer(client, Session, started.json(), True).json()['result']['score'] == count
