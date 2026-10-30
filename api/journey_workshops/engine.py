"""Pure v1 workshop replay. Evidence is authored, not a measured risk/mastery score.

Keep this resolver for existing snapshots. New mechanics need a new revision;
clients submit only one offered choice and never submit findings or outcomes.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictInt

STAGES = ('discover','understand','check','investigate','defend','command','opponent','compete')


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Choice(StrictModel):
    id: Literal['a', 'b']
    label: str = Field(min_length=5, max_length=200)
    explanation: str = Field(min_length=10, max_length=700)
    effort: StrictInt = Field(ge=0, le=3)
    fact: str | None = Field(max_length=700)


class Step(StrictModel):
    prompt: str = Field(min_length=10, max_length=400)
    context: str = Field(min_length=10, max_length=400)
    choices: list[Choice] = Field(min_length=2, max_length=2)


class Case(StrictModel):
    id: str = Field(pattern=r'^[a-z][a-z0-9-]{0,47}$')
    revision: Literal['workshops-v1']
    stage: Literal['discover','understand','check','investigate','defend','command','opponent','compete']
    title: str = Field(min_length=3, max_length=100)
    briefing: str = Field(min_length=10, max_length=700)
    objective: str = Field(min_length=10, max_length=700)
    steps: list[Step] = Field(min_length=3, max_length=3)


def validate(snapshot):
    case = Case.model_validate(snapshot)
    if any({c.id for c in step.choices} != {'a','b'} for step in case.steps):
        raise ValueError('Two distinct workshop choices required')
    return case.model_dump()


CASES = {}
for _snapshot in json.loads((Path(__file__).parents[1] / 'content/journey_workshops_v1.json').read_text(encoding='utf-8')):
    _case = validate(_snapshot)
    if _case['id'] in CASES:
        raise ValueError('Duplicate workshop identifier')
    CASES[_case['id']] = _case
if len(CASES) != 24 or any(sum(c['stage']==s for c in CASES.values())!=3 for s in STAGES):
    raise ValueError('Each journey stage requires three reviewed workshops')


def new_state(snapshot, baseline=None):
    return {'snapshot':validate(snapshot),'decisions':[],'receipts':{},'baseline':deepcopy(baseline)}


def project(state):
    case = validate(state['snapshot'])
    decisions = state['decisions']
    if len(decisions)>3 or any(c not in ('a','b') for c in decisions):
        raise ValueError('Invalid workshop history')
    recap, findings, unresolved, effort = [], [], [], 0
    for index, choice_id in enumerate(decisions):
        choice = next(c for c in case['steps'][index]['choices'] if c['id']==choice_id)
        effort += choice['effort']
        recap.append({'step':index+1,'prompt':case['steps'][index]['prompt'], **deepcopy(choice)})
        (findings if choice['fact'] else unresolved).append(choice['fact'] or choice['explanation'])
    step = None
    if len(decisions)<3:
        raw = case['steps'][len(decisions)]
        options = [{'id':c['id'],'label':c['label'],'effort':c['effort']} for c in raw['choices']]
        # Vary display position across cases/steps, preserving stable replay.
        if int(sha256(f"{case['id']}:{len(decisions)}".encode()).hexdigest()[:2],16)%2:
            options.reverse()
        step = {'prompt':raw['prompt'],'context':raw['context'],'choices':options}
    return {'case_id':case['id'],'revision':case['revision'],'stage':case['stage'],'title':case['title'],
            'briefing':case['briefing'],'objective':case['objective'],'step_index':len(decisions),
            'completed':len(decisions)==3,'step':step,'recap':recap,'findings':findings,
            'unresolved':unresolved,'effort':effort,'baseline':deepcopy(state.get('baseline')),
            'notice':'Fixed authored case consequences and simplified effort units; findings and completion are not a cybersecurity mastery score.'}


def advance(state, choice_id, expected_step, command_id):
    fingerprint = {'choice_id':choice_id,'expected_step':expected_step}
    receipt = state['receipts'].get(command_id)
    if receipt is not None:
        if receipt != fingerprint:
            raise ValueError('Command ID already used for different input')
        return deepcopy(state)
    if expected_step != len(state['decisions']) or expected_step>=3:
        raise ValueError('Workshop changed or finished; reload the saved activity')
    if choice_id not in {c['id'] for c in project(state)['step']['choices']}:
        raise ValueError('Choice unavailable')
    result = deepcopy(state)
    result['decisions'].append(choice_id)
    result['receipts'][command_id]=fingerprint
    return result


def summary(state):
    p=project(state)
    if not p['completed']: raise ValueError('Finish the workshop before comparison')
    return {k:p[k] for k in ('effort','findings','unresolved')}
