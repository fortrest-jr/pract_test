import pytest

from src.Config import MAX_FRAGILE_DISTANCE
from src.Errors import NEGATIVE_DISTANCE_ERROR, NEGATIVE_SIZE_ERROR, DISTANCE_EXCEED_WITH_FRAGILE_ERROR
from src.__main__ import validate_params


@pytest.fixture()
def default_params() -> dict[str, int | bool]:
    return {
        'distance': 1,
        'size': 1,
        'fragile': False
    }


@pytest.mark.parametrize('negative_distance',[
    -0.1,
    -1,
    -100
])
def test_negative_distance_raises_exception(default_params, negative_distance) -> None:
    params = {
        **default_params,
        'distance': negative_distance
    }

    expected_message = NEGATIVE_DISTANCE_ERROR.format(value=negative_distance)
    with pytest.raises(ValueError, match=expected_message):
        validate_params(**params)


@pytest.mark.parametrize('negative_size',[
    -0.1,
    -1,
    -100
])
def test_negative_size_raises_exception(default_params, negative_size) -> None:
    params = {
        **default_params,
        'size': negative_size
    }

    expected_message = NEGATIVE_SIZE_ERROR.format(value=negative_size)
    with pytest.raises(ValueError, match=expected_message):
        validate_params(**params)


@pytest.mark.parametrize('distance_exceedance', [
    0.1,
    1,
    100
])
def test_big_distance_with_fragile_raises_exception(default_params, distance_exceedance) -> None:
    exceed_distance = MAX_FRAGILE_DISTANCE + distance_exceedance
    params = {
        **default_params,
        'fragile': True,
        'distance': exceed_distance
    }

    expected_message = DISTANCE_EXCEED_WITH_FRAGILE_ERROR.format(value=exceed_distance, max_distance=MAX_FRAGILE_DISTANCE)
    with pytest.raises(ValueError, match=expected_message):
        validate_params(**params)


def test_many_exceptions_rise() -> None:
    negative_size = -1
    exceed_distance = MAX_FRAGILE_DISTANCE + 1
    params = {
        'size': negative_size,
        'distance': exceed_distance,
        'fragile': True
    }

    expected_messages = [
        NEGATIVE_SIZE_ERROR.format(value=negative_size),
        DISTANCE_EXCEED_WITH_FRAGILE_ERROR.format(value=exceed_distance, max_distance=MAX_FRAGILE_DISTANCE)
    ]
    with pytest.raises(ValueError) as exc_info:
        validate_params(**params)

    for exception_message in expected_messages:
        assert exception_message in str(exc_info.value), f'missing ValueError {exception_message}'
