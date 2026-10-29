"""Owned, bounded saved decision workshops, independent of existing progress."""
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import JourneyWorkshopRun
from db_dependencies import get_db
from learning_routes import student_only
from cyber_lab_routes import creation_limit, owned
from red_blue_routes import BoundedRoute, private_response, persist
from journey_workshops import engine

router=APIRouter(prefix='/api/v1/workshops',tags=['workshops'],route_class=BoundedRoute,
                 dependencies=[Depends(private_response)])


class Start(BaseModel):
    model_config=ConfigDict(extra='forbid')
    case_id: str = Field(min_length=1,max_length=48,pattern=r'^[a-z][a-z0-9-]*$')
    replay_of: StrictInt | None = Field(default=None,ge=1,le=2_147_483_647)


class Decision(BaseModel):
    model_config=ConfigDict(extra='forbid')
    command_id: UUID
    expected_step: StrictInt = Field(ge=0,le=2)
    choice_id: Literal['a','b']


def public(row):
    try: return {'id':row.id,**engine.project(row.state)}
    except (ValueError,KeyError,TypeError):
        raise HTTPException(409,'Saved workshop requires maintainer review') from None


@router.get('/catalog')
def catalog():
    return {'revision':'workshops-v1','cases':[{k:c[k] for k in ('id','title','stage','briefing','objective')}
                                            for c in engine.CASES.values()]}


@router.post('/runs',status_code=201)
def start(body:Start,user=Depends(student_only),db:Session=Depends(get_db)):
    case=engine.CASES.get(body.case_id)
    if case is None: raise HTTPException(422,'Unknown workshop')
    creation_limit(db,JourneyWorkshopRun,user.id)
    baseline=None
    if body.replay_of is not None:
        parent=owned(db,JourneyWorkshopRun,user.id,body.replay_of)
        if parent.state['snapshot']['id']!=body.case_id:
            raise HTTPException(422,'Choose the same workshop for a comparison')
        try: baseline=engine.summary(parent.state)
        except ValueError: raise HTTPException(409,'Finish the earlier workshop first') from None
        case=parent.state['snapshot']  # Exact original edition and opening.
    row=JourneyWorkshopRun(user_id=user.id,state=engine.new_state(case,baseline))
    db.add(row);persist(db,label='Workshop')
    return public(row)


@router.get('/runs')
def history(before_id:int|None=Query(None,ge=1),user=Depends(student_only),db:Session=Depends(get_db)):
    stmt=select(JourneyWorkshopRun).where(JourneyWorkshopRun.user_id==user.id)
    if before_id:stmt=stmt.where(JourneyWorkshopRun.id<before_id)
    rows=db.scalars(stmt.order_by(JourneyWorkshopRun.id.desc()).limit(21)).all()
    return {'runs':[{'id':r.id,**{k:public(r)[k] for k in ('title','case_id','stage','completed','step_index')}} for r in rows[:20]],
            'next_before_id':rows[19].id if len(rows)>20 else None}


@router.get('/runs/{run_id}')
def resume(run_id:int,user=Depends(student_only),db:Session=Depends(get_db)):
    return public(owned(db,JourneyWorkshopRun,user.id,run_id))


@router.post('/runs/{run_id}/decisions')
def decide(run_id:int,body:Decision,user=Depends(student_only),db:Session=Depends(get_db)):
    row=owned(db,JourneyWorkshopRun,user.id,run_id,lock=True)
    try: row.state=engine.advance(row.state,body.choice_id,body.expected_step,str(body.command_id))
    except ValueError as error: raise HTTPException(409,str(error)) from None
    persist(db,label='Workshop')
    return public(row)
