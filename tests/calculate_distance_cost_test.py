import pytest

from src.Config import DISTANCE_COSTS
from src.__main__ import calculate_distance_cost
from src.Errors import CANNOT_GET_VALUE_FROM_INTERVAL_ERROR
from tests.conftest import EPSILON


@pytest.mark.parametrize(
    'distance, expected_cost',
    [
        (1, 50),
        (7, 100),
        (20, 200),
        (35.0, 300),
    ],
)
def test_calculate_distance_cost_returns_correct_cost(distance, expected_cost):
    result = calculate_distance_cost(distance)
    assert result == expected_cost


@pytest.mark.parametrize(
    'distance',
    [
        -1.0,
        -0.1,
        -100.0,
    ],
)
def test_calculate_distance_cost_raises_on_negative_distance(distance):
    param_name = 'distance'
    lowest_value = sorted(DISTANCE_COSTS.keys())[0]
    expected_message = CANNOT_GET_VALUE_FROM_INTERVAL_ERROR.format(
        param_name=param_name, param_value=distance, lowest_value=lowest_value
    )
    with pytest.raises(ValueError, match=expected_message):
        calculate_distance_cost(distance)


@pytest.mark.parametrize('distance, expected_cost', DISTANCE_COSTS.items())
def test_calculate_distance_cost_at_boundary_from_interval_values(distance, expected_cost):
    result = calculate_distance_cost(distance)
    assert result == expected_cost


LOWER_BOUNDARIES = [(float(distance), cost) for distance, cost in DISTANCE_COSTS.items()]
UPPER_BOUNDARIES = [
    (upper_distance - EPSILON, cost)
    for upper_distance, cost in zip(list(DISTANCE_COSTS.keys())[1:], DISTANCE_COSTS.values())
]
BOUNDARIES = LOWER_BOUNDARIES + UPPER_BOUNDARIES


@pytest.mark.parametrize('distance, expected_cost', BOUNDARIES)
def test_calculate_distance_cost_at_boundary_values(distance, expected_cost):
    result = calculate_distance_cost(distance)
    assert result == expected_cost
