import pytest

from src.Config import SIZE_COSTS
from src.ErrorMessages import CANNOT_GET_VALUE_FROM_INTERVAL_ERROR
from src.__main__ import calculate_size_cost
from tests.helpers import generate_boundaries_from_interval


@pytest.mark.parametrize(
    'size, expected_cost',
    [
        (1.5, 100),
        (3.5, 200),
    ],
)
def test_calculate_size_cost_returns_correct_cost(size, expected_cost):
    result = calculate_size_cost(size)
    assert result == expected_cost


@pytest.mark.parametrize(
    'invalid_size',
    [-1.0, -0.5]
)
def test_calculate_size_cost_raises_on_invalid_size(invalid_size):
    param_name = 'size'
    lowest_value = sorted(SIZE_COSTS.keys())[0]
    expected_message = CANNOT_GET_VALUE_FROM_INTERVAL_ERROR.format(
        param_name=param_name, param_value=invalid_size, lowest_value=lowest_value
    )

    with pytest.raises(ValueError, match=expected_message):
        calculate_size_cost(invalid_size)


@pytest.mark.parametrize('size, expected_cost', generate_boundaries_from_interval(SIZE_COSTS))
def test_calculate_size_cost_at_boundary_values(size, expected_cost):
    result = calculate_size_cost(size)
    assert result == expected_cost
