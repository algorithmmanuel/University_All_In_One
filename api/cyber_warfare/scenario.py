"""Strict local configuration loading, with immutable validated snapshots."""
import hashlib
import json
import re
from pathlib import Path
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Identifier = Annotated[str, Field(pattern=r'^[a-z][a-z0-9_\-]{0,47}$')]
SmallText = Annotated[str, Field(min_length=1, max_length=500)]
Control = Literal['monitoring', 'patched', 'hardened', 'segmented', 'access_control', 'backup']
Weakness = Literal['phishing', 'privilege', 'configuration', 'access', 'instruction']


class Schema(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, strict=True)


class Asset(Schema):
    id: Identifier
    name: SmallText
    kind: Literal['workstation', 'server', 'database', 'cloud', 'third_party']
    value: Annotated[int, Field(ge=1, le=100)]
    exposed: bool
    vulnerabilities: tuple[Weakness, ...]
    controls: tuple[Control, ...]
    initial_access: Annotated[int, Field(ge=0, le=2)] = 0


class Connection(Schema):
    source: Identifier
    target: Identifier


class Intelligence(Schema):
    known_assets: tuple[Identifier, ...]
    briefing: SmallText


class Objective(Schema):
    kind: Literal['fraud', 'leak', 'disruption']
    targets: Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=20)]
    threshold: Annotated[int, Field(ge=1, le=2000)]
    hold_turns: Annotated[int, Field(ge=1, le=30)] = 1
    explanation: SmallText


class Scenario(Schema):
    schema_version: Literal[1]
    id: Identifier
    revision: Annotated[int, Field(ge=1, le=10000)]
    title: SmallText
    industry: SmallText
    difficulty: Literal['beginner', 'intermediate', 'advanced']
    turn_limit: Annotated[int, Field(ge=3, le=30)]
    action_points: Annotated[int, Field(ge=3, le=6)]
    starting_budget: Annotated[int, Field(ge=6, le=100)]
    assets: Annotated[tuple[Asset, ...], Field(min_length=2, max_length=20)]
    connections: Annotated[tuple[Connection, ...], Field(max_length=60)]
    red: Intelligence
    blue: Intelligence
    objective: Objective

    @model_validator(mode='after')
    def consistent(self):
        ids = {a.id for a in self.assets}
        if len(ids) != len(self.assets):
            raise ValueError('Duplicate asset id')
        if any(not set(i.known_assets) <= ids or len(set(i.known_assets)) != len(i.known_assets) for i in (self.red, self.blue)):
            raise ValueError('Unknown intelligence asset')
        if set(self.blue.known_assets) != ids:
            raise ValueError('Blue owns the entire inventory')
        if not set(self.objective.targets) <= ids or len(set(self.objective.targets)) != len(self.objective.targets):
            raise ValueError('Invalid objective targets')
        if self.objective.threshold > sum(a.value for a in self.assets if a.id in self.objective.targets):
            raise ValueError('Unreachable objective threshold')
        if self.objective.hold_turns > self.turn_limit:
            raise ValueError('Unreachable holding period')
        if self.objective.kind != 'disruption' and self.objective.hold_turns != 1:
            raise ValueError('Holding periods apply only to disruption')
        edges = [(e.source, e.target) for e in self.connections]
        if len(set(edges)) != len(edges) or any(s not in ids or t not in ids or s == t for s, t in edges):
            raise ValueError('Invalid or duplicate connection')
        for a in self.assets:
            if len(set(a.controls)) != len(a.controls) or len(set(a.vulnerabilities)) != len(a.vulnerabilities):
                raise ValueError('Duplicate control or vulnerability')
            if a.initial_access and a.id not in self.red.known_assets:
                raise ValueError('Starting foothold must be known to Red')
        return self

    def snapshot(self):
        return self.model_dump(mode='json')

    def digest(self):
        return hashlib.sha256(json.dumps(self.snapshot(), sort_keys=True).encode()).hexdigest()


DIRECTORY = Path(__file__).parent / 'scenarios'


def parse_scenario(snapshot):
    # JSON validation allows JSON arrays for immutable tuple fields; all other types remain strict.
    return Scenario.model_validate_json(json.dumps(snapshot, allow_nan=False))


def load_scenario(scenario_id):
    if not isinstance(scenario_id, str) or not re.fullmatch(r'[a-z][a-z0-9_\-]{0,47}', scenario_id):
        raise ValueError('Invalid scenario id')
    path = DIRECTORY / f'{scenario_id}.json'
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 64000:
        raise ValueError('Unknown or oversized scenario')
    scenario = Scenario.model_validate_json(path.read_text(encoding='utf-8'))
    if scenario.id != scenario_id:
        raise ValueError('Scenario id does not match filename')
    return scenario


def list_scenarios():
    return tuple(load_scenario(p.stem) for p in sorted(DIRECTORY.glob('*.json')))
