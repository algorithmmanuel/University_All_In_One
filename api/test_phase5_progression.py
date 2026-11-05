"""Phase 5 read-only mission evidence and owned history pagination regressions."""
from datetime import datetime, timezone
from test_mission_learning import mission_client
from test_foundations_courses import content_state


def test_mission_activity_counts_distinct_completions_and_latest_active_only(mission_client):
    from models import MissionRun
    client, Session, learner = mission_client
    before = client.get('/api/v1/missions/progress').json()
    assert (before['completed_missions'], before['active_missions'], before['available_missions']) == (1, 1, 30)
    with Session.begin() as db:
        db.add(MissionRun(id=3,user_id=1,mission_id='phishing-investigation',step_index=3,score=45,choices=[],completed_at=datetime.now(timezone.utc)))
        db.add(MissionRun(id=4,user_id=2,mission_id='soc-alert-triage',step_index=0,score=0,choices=[]))
    body = client.get('/api/v1/missions/progress').json()
    assert body['completed_missions'] == 1 and body['active_missions'] == 0
    assert len(body['recent_missions']) == 1 and body['recent_missions'][0]['run_id'] == 3
    learner.id = 2
    body = client.get('/api/v1/missions/progress').json()
    assert body['completed_missions'] == 0 and body['recent_missions'][0]['run_id'] == 4
    learner.role='teacher'
    assert client.get('/api/v1/missions/progress').status_code == 403


def test_saved_decision_recap_uses_original_feedback_without_regrading(mission_client):
    from models import MissionRun
    client, Session, _ = mission_client
    with Session.begin() as db:
        db.get(MissionRun,1).choices=[{'step':0,'points':5,'feedback':'Original saved reasoning'},
            {'step':1,'points':15,'feedback':'Original second decision'}, {'step':2,'feedback':'Legacy detail'},
            {'step':3,'points':15,'feedback':'Uncommitted future stage'}]
    body=client.get('/api/v1/missions/runs/1').json()
    assert body['score']==20
    recap=body['decision_recap']
    assert len(recap)==3 and recap[0]['feedback']=='Original saved reasoning'
    assert [row['points'] for row in recap]==[5,15,None]
    assert 'Review' in recap[0]['next_step'] and 'unavailable' in recap[2]['next_step']
    assert client.get('/api/v1/missions/runs/1').json()['decision_recap']==recap
    with Session() as db:
        assert db.get(MissionRun,1).score==20 and len(db.get(MissionRun,1).choices)==4


def test_older_mission_history_is_owned_complete_and_nonduplicating(mission_client):
    from models import MissionRun
    client,Session,learner=mission_client
    with Session.begin() as db:
        for i in range(3,58):db.add(MissionRun(id=i,user_id=1,mission_id='phishing-investigation',step_index=0,score=0,choices=[]))
        db.add(MissionRun(id=100,user_id=2,mission_id='phishing-investigation',step_index=0,score=0,choices=[]))
    first=client.get('/api/v1/missions/history').json()
    assert len(first['runs'])==50 and first['next_before_id'] is not None
    second=client.get('/api/v1/missions/history',params={'before_id':first['next_before_id']}).json()
    ids=[row['id'] for row in first['runs']+second['runs']]
    assert len(ids)==len(set(ids))==57 and 100 not in ids and second['next_before_id'] is None
    assert client.get('/api/v1/missions/history?before_id=0').status_code==422
    learner.id=2
    assert [r['id'] for r in client.get('/api/v1/missions/history').json()['runs']]==[100]


def test_older_assessment_pagination_uses_saved_chronology_and_ownership(content_state):
    from models import QuizAttempt, Enrollment
    client,Session,learner=content_state
    with Session.begin() as db:
        # Deliberately reverse ID/date order: an ID-only cursor would lose rows.
        for i in range(100,145):db.add(QuizAttempt(id=i,user_id=1,course_id=1,answers={},score=0,total=1,
            submitted_at=datetime(2025,1,1+(144-i)//2,tzinfo=timezone.utc)))
        db.add(QuizAttempt(id=200,user_id=2,course_id=1,answers={},score=1,total=1))
        db.add(Enrollment(user_id=2,course_id=1))
    output=[];cursor=None
    for _ in range(4):
        page=client.get('/api/v1/quizzes/courses/1/attempts',params={'before_id':cursor} if cursor else {}).json()
        output.extend(a['id'] for a in page['attempts']);cursor=page['next_before_id']
        if cursor is None:break
    assert len(output)==len(set(output))==46 and 200 not in output
    assert client.get('/api/v1/quizzes/courses/1/attempts?before_id=200').status_code==404
    assert client.get('/api/v1/quizzes/courses/1/attempts?before_id=2').status_code==404
    assert client.get('/api/v1/quizzes/courses/1/attempts?before_id=0').status_code==422
