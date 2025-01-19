import pytest

from src.Config import DISTANCE_COSTS
from src.__main__ import calculate_distance_cost
from src.Errors import CANNOT_GET_VALUE_FROM_INTERVAL_ERROR

@pytest.mark.parametrize('distance, expected_cost', [
    (5.5, 100),
    (15.5, 200),
    (25.5, 300),
    (35.0, 400),
])
def test_calculate_distance_cost_returns_correct_cost(distance, expected_cost):
    result = calculate_distance_cost(distance)
    assert result == expected_cost

@pytest.mark.parametrize('distance', [
    -1.0,
    -0.1,
    -100.0,
])
def test_calculate_distance_cost_raises_on_negative_distance(distance):
    param_name = 'distance'
    lowest_value = sorted(DISTANCE_COSTS.keys())[0]
    expected_message = CANNOT_GET_VALUE_FROM_INTERVAL_ERROR.format(
        param_name=param_name,
        param_value=distance,
        lowest_value=lowest_value)
    with pytest.raises(ValueError, match=expected_message):
        calculate_distance_cost(distance)

@pytest.mark.parametrize('distance, expected_cost', [
    (0.0, 100),
    (10.0, 200),
    (20.0, 300),
    (30.0, 400),
])
def test_calculate_distance_cost_at_boundary_values(distance, expected_cost):
    result = calculate_distance_cost(distance)
    assert result == expected_cost
