import pytest

from src.Config import FRAGILE_COSTS
from src.__main__ import calculate_fragile_cost


@pytest.mark.parametrize('fragile, expected_cost', [
    (True, FRAGILE_COSTS[True]),
    (False, FRAGILE_COSTS[False])
])
def test_calculate_fragile_cost_returns_correct_value(fragile, expected_cost):
    result = calculate_fragile_cost(fragile)
    assert result == expected_cost
