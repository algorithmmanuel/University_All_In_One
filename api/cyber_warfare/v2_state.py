"""Isolated Red/Blue V2 observation types. Legacy engine remains unchanged.

Internal engine-issued evidence and private truth MUST NOT be serialized to clients.
The rule reducer, clock and event generation will be separately implemented.
"""
from dataclasses import dataclass
from typing import Literal
from .v2_validation import validate_match

Side = Literal['red', 'blue']
Knowledge = Literal['confirmed', 'suspected', 'stale', 'unknown']


@dataclass(frozen=True)
class Capability:
    id: str
    owner: Side
    asset_id: str
    evidence_kinds: frozenset[str] = frozenset()
    action_ids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class AssetTruth:
    id: str
    name: str
    kind: str
    value: int
    available: bool
    blue_controls: tuple[str, ...] = ()
    red_access: int = 0
    persistent: bool = False


@dataclass(frozen=True)
class Evidence:
    """Trusted internal event with an explicit maximum audience and sensor gate."""
    id: str
    turn: int
    asset_id: str
    kind: str
    text: str
    visible_to: frozenset[Side]
    certainty: Knowledge
    required_capability: str | None = None


@dataclass(frozen=True)
class SeatKnowledge:
    asset_id: str
    status: Knowledge
    last_observed_turn: int | None = None
    red_access: int | None = None


@dataclass(frozen=True)
class MatchTruth:
    edition: Literal['red-blue-v2']
    turn: int
    assets: tuple[AssetTruth, ...]
    capabilities: tuple[Capability, ...]
    evidence: tuple[Evidence, ...]
    blue_inventory: frozenset[str]
    red_known: frozenset[str]
    red_knowledge: tuple[SeatKnowledge, ...] = ()


def project_for_seat(match: MatchTruth, side: Side) -> dict:
    """Make a JSON-safe projection without copying opponent-private match truth.

    Event generation and event audience assignment must be performed by the
    trusted engine, never client input. Capability matching can only restrict
    an event's explicit audience, never grant a new one.
    """
    if side not in ('red', 'blue'):
        raise ValueError('Unknown seat')
    if match.edition != 'red-blue-v2':
        raise ValueError('Unsupported edition')
    if not isinstance(match, MatchTruth):
        raise ValueError('V2 match required')
    validate_match(match)
    inventory = match.blue_inventory if side == 'blue' else match.red_known
    truths = {a.id: a for a in match.assets}
    own_capabilities = tuple(c for c in match.capabilities if c.owner == side)
    knowledge = {k.asset_id: k for k in match.red_knowledge}
    assets = []
    for asset_id in sorted(inventory):
        if asset_id not in truths:
            raise ValueError('Unknown asset in inventory')
        a = truths[asset_id]
        events = []
        for ev in match.evidence:
            if ev.asset_id != asset_id or side not in ev.visible_to:
                continue
            if ev.required_capability is not None and not any(
                c.asset_id == asset_id and ev.required_capability in c.evidence_kinds
                for c in own_capabilities
            ):
                continue
            events.append({'id': ev.id, 'turn': ev.turn, 'kind': ev.kind,
                           'message': ev.text, 'certainty': ev.certainty})
        events.sort(key=lambda event: (event['turn'], event['id']))
        item = {'id': a.id, 'name': a.name, 'kind': a.kind,
                'value': a.value, 'events': events}
        if side == 'blue':
            item.update(available=a.available, controls=list(a.blue_controls),
                        knowledge='confirmed')
        else:
            k = knowledge.get(asset_id)
            item.update(knowledge=k.status if k else 'unknown',
                        observed_turn=k.last_observed_turn if k else None,
                        access=k.red_access if k else None)
        assets.append(item)
    return {'edition': match.edition, 'turn': match.turn, 'side': side,
            'assets': assets,
            'capabilities': [{'id': c.id, 'asset_id': c.asset_id,
                              'action_ids': sorted(c.action_ids)}
                             for c in own_capabilities]}
