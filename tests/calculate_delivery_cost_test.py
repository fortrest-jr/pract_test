from collections import namedtuple

import pytest
from allpairspy import AllPairs

from typing import TypeVar

from src.Config import DISTANCE_COSTS, SIZE_COSTS, FRAGILE_COSTS, WORKLOAD_MULTIPLIERS
from src.Workload import Workload
from src.__main__ import calculate_delivery_cost, MINIMAL_COST

T = TypeVar('T')
value_cost = namedtuple('vc', 'value cost')


@pytest.mark.parametrize('distance, size, fragile, workload', [
    (0.1, 0.1, False, Workload.NORMAL),
    (29.9, 1.9, False, Workload.MODERATE),
    (9.9, 2, False, Workload.MODERATE)
])
def test_minimal_cost_applied_when_lower(distance: float, size: float, fragile: bool, workload: Workload):
    result_cost = calculate_delivery_cost(distance, size, fragile, workload)
    assert result_cost == MINIMAL_COST


@pytest.mark.parametrize('distance, size, fragile, workload, expected_cost', [
    (10, 2, False, Workload.NORMAL, 400.),
    (30, 2, True, Workload.VERY_HIGH, 1280.)
])
def test_counting_cost(distance: float, size: float, fragile: bool, workload: Workload, expected_cost: float):
    result_cost = calculate_delivery_cost(distance, size, fragile, workload)
    assert result_cost == pytest.approx(expected_cost)




def get_value_cost_pairs_from_interval_dict(interval_dict: dict[T:(int, bool, Workload), int]) -> list[value_cost[T, int]]:
    return [value_cost(value, cost) for value, cost in interval_dict.items()]


all_params_value_costs = [
    value_cost_pairs
    for value_cost_pairs in AllPairs(
        [
            get_value_cost_pairs_from_interval_dict(DISTANCE_COSTS),
            get_value_cost_pairs_from_interval_dict(SIZE_COSTS),
            get_value_cost_pairs_from_interval_dict(FRAGILE_COSTS),
            get_value_cost_pairs_from_interval_dict(WORKLOAD_MULTIPLIERS),
        ]
    )
]


def simple_cost_calculator(
        distance: value_cost[int, int],
        size: value_cost[int, int],
        fragile: value_cost[bool, int],
        workload: value_cost[Workload, float]):
    return (distance.cost + size.cost + fragile.cost) * workload.cost


@pytest.mark.parametrize('distance, size, fragile, workload', all_params_value_costs)
def test_cost_on_boundaries(
        distance: value_cost[int, int],
        size: value_cost[int, int],
        fragile: value_cost[bool, int],
        workload: value_cost[Workload, float]):
    calculated_cost = simple_cost_calculator(distance, fragile, size, workload)
    expected_result = calculated_cost if calculated_cost >= MINIMAL_COST else MINIMAL_COST

    result = calculate_delivery_cost(distance.value, size.value, fragile.value, workload.value)

    assert result == expected_result
