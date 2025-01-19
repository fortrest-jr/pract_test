import pytest

from src.Workload import Workload


@pytest.fixture()
def default_params() -> dict[str, int | bool]:
    return {
        'distance': 1,
        'size': 1,
        'fragile': False,
        'workload': Workload.MODERATE
    }