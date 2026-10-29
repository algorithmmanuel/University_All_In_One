"""Current selectable scenarios; historical rule modules remain unchanged."""
from strategy_scenarios import SCENARIOS as LEGACY_SCENARIOS
from strategy_siege import INFO

SCENARIOS = {**LEGACY_SCENARIOS, 'siege': INFO}
