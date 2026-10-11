"""Versioned public mission manifests for 2D and future 3D clients.

Do not expose server-owned scoring keys, answer points, or feedback before decisions.
This module adapts legacy mission content without changing stored mission runs.
"""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from mission_data import MISSIONS
from pathway_catalog import PATHWAYS

class MissionManifest(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str = Field(min_length=1)
    version: int = Field(ge=1)
    pathway: Literal["secondary", "university", "professional"]
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    difficulty: str = Field(min_length=1)
    scene_type: Literal["decision", "3d-soc"]
    step_count: int = Field(ge=1)
    max_score: int = Field(ge=0)

def build_manifest(mission_id: str) -> MissionManifest:
    mission = MISSIONS[mission_id]
    pathway = next(
        (p.id for p in PATHWAYS if mission_id in p.sample_missions), None
    )
    if pathway is None:
        raise ValueError(f"Mission has no pathway: {mission_id}")
    steps = mission["steps"]
    if not steps:
        raise ValueError(f"Mission has no steps: {mission_id}")
    for step in steps:
        if not step["options"] or not step["evidence"]:
            raise ValueError(f"Mission has an incomplete step: {mission_id}")
    return MissionManifest(
        id=mission_id,
        version=1,
        pathway=pathway,
        title=mission["title"],
        summary=mission["summary"],
        difficulty=mission["difficulty"],
        scene_type="decision",
        step_count=len(steps),
        max_score=15 * len(steps),
    )

def public_manifest_catalog() -> dict:
    return {"version": 1, "missions": [
        build_manifest(mission_id).model_dump(mode="json")
        for mission_id in MISSIONS
    ]}
