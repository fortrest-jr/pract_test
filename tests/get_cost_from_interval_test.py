import pytest

from src.Errors import CANNOT_GET_VALUE_FROM_INTERVAL_ERROR
from src.__main__ import get_cost_from_interval


@pytest.mark.parametrize('intervals, value, expected_cost', [
    ({10: 100, 20: 200, 30: 300}, 15, 100),
    ({10: 100, 20: 200, 30: 300}, 25, 200),
    ({10: 100, 20: 200, 30: 300}, 35, 300),
    ({0: 50, 100: 100, 1000: 200}, 50, 50),
    ({0: 50, 100: 100, 1000: 200}, 500, 100),
])
def test_get_cost_from_interval_returns_correct_cost(intervals, value, expected_cost):
    result = get_cost_from_interval(intervals, value, "test_param")
    assert result == expected_cost


@pytest.mark.parametrize('intervals, value, expected_cost', [
    ({10: 100}, 10, 100),
    ({10: 100}, 11, 100),
    ({0: 50}, 0, 50),
    ({0: 50}, 1000, 50),
])
def test_get_cost_from_interval_single_interval(intervals, value, expected_cost):
    result = get_cost_from_interval(intervals, value, "test_param")
    assert result == expected_cost


@pytest.mark.parametrize('intervals, value', [
    ({10: 100, 20: 200}, 5),
    ({100: 100, 200: 200}, 50),
    ({1: 100, 2: 200}, 0),
    ({0.1: 100, 0.2: 200}, 0.05),
])
def test_get_cost_from_interval_raises_on_too_small_value(intervals, value):
    param_name = 'test_param'
    lowest_value = sorted(intervals.keys())[0]
    expected_message = CANNOT_GET_VALUE_FROM_INTERVAL_ERROR.format(
        param_name=param_name,
        param_value=value,
        lowest_value=lowest_value)
    with pytest.raises(ValueError, match=expected_message):
        get_cost_from_interval(intervals, value, param_name)
