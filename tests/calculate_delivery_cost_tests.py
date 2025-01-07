import pytest

from src.Workload import Workload
from src.__main__ import calculate_delivery_cost, MINIMAL_COST

@pytest.mark.parametrize('distance, size, fragile, workload', [
    (0.1, 0.1, False, Workload.NORMAL),
    (29.9, 1.9, False, Workload.MODERATE),
    (9.9, 2, False, Workload.MODERATE)
])
def test_minimal_cost_applied_when_lower(distance: float, size: float, fragile: bool, workload: Workload):
    result_cost = calculate_delivery_cost(distance, size, fragile, workload)
    expected_cost = MINIMAL_COST
    assert result_cost == expected_cost

@pytest.mark.parametrize('distance, size, fragile, workload, expected_cost', [
    (10, 2, False, Workload.NORMAL, 400.),
    (30, 2, True, Workload.VERY_HIGH, 1280.)
])
def test_counting_cost(distance: float, size: float, fragile: bool, workload: Workload, expected_cost: float):
    result_cost = calculate_delivery_cost(distance, size, fragile, workload)
    assert result_cost == pytest.approx(expected_cost)
