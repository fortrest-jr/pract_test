import pytest
from src.Workload import Workload
from src.__main__ import calculate_workload_multiplier
from src.Config import WORKLOAD_MULTIPLIERS


@pytest.mark.parametrize(
    'workload, expected_multiplier',
    [
        (Workload.MODERATE, WORKLOAD_MULTIPLIERS[Workload.MODERATE]),
        (Workload.HIGH, WORKLOAD_MULTIPLIERS[Workload.HIGH]),
        (Workload.VERY_HIGH, WORKLOAD_MULTIPLIERS[Workload.VERY_HIGH]),
    ],
)
def test_valid_workload_multipliers(workload, expected_multiplier) -> None:
    result = calculate_workload_multiplier(workload)
    assert result == expected_multiplier


def test_normal_workload_returns_default() -> None:
    result = calculate_workload_multiplier(Workload.NORMAL)
    expected_multiplier = WORKLOAD_MULTIPLIERS['DEFAULT']
    assert result == expected_multiplier


@pytest.mark.parametrize('invalid_workload', ["INVALID", None, False])
def test_invalid_workload_returns_default(invalid_workload) -> None:
    result = calculate_workload_multiplier(invalid_workload)
    expected_multiplier = WORKLOAD_MULTIPLIERS['DEFAULT']
    assert result == expected_multiplier
