import pytest

from src.Config import MAX_FRAGILE_DISTANCE
from src.ErrorMessages import NEGATIVE_DISTANCE_ERROR, NEGATIVE_SIZE_ERROR, DISTANCE_EXCEED_WITH_FRAGILE_ERROR
from src.__main__ import validate_params
from tests.helpers import MINIMAL_TEST_VALUE


@pytest.fixture()
def default_params() -> dict[str, int | bool]:
    return {
        'distance': 1,
        'size': 1,
        'fragile': False
    }


@pytest.mark.parametrize('valid_distance,valid_size', [
    (0, 0),
    (MINIMAL_TEST_VALUE, MINIMAL_TEST_VALUE),
    (1000, 1000),
    (float('inf'), float('inf'))
])
def test_valid_positive_values_pass(default_params, valid_distance, valid_size) -> None:
    params = {
        **default_params,
        'distance': valid_distance,
        'size': valid_size
    }
    validate_params(**params)


def test_large_distance_with_non_fragile_passes(default_params) -> None:
    params = {
        **default_params,
        'distance': MAX_FRAGILE_DISTANCE * 10,
        'fragile': False
    }
    validate_params(**params)


def test_max_fragile_distance_boundary(default_params) -> None:
    params = {
        **default_params,
        'distance': MAX_FRAGILE_DISTANCE,
        'fragile': True
    }
    validate_params(**params)


@pytest.mark.parametrize('negative_distance', [
    -MINIMAL_TEST_VALUE,
    -1,
    -100
])
def test_negative_distance_raises_exception(default_params, negative_distance) -> None:
    params = {**default_params, 'distance': negative_distance}

    expected_message = NEGATIVE_DISTANCE_ERROR.format(value=negative_distance)
    with pytest.raises(ValueError, match=expected_message):
        validate_params(**params)


@pytest.mark.parametrize('negative_size', [
    -MINIMAL_TEST_VALUE,
    -1,
    -100
])
def test_negative_size_raises_exception(default_params, negative_size) -> None:
    params = {**default_params, 'size': negative_size}

    expected_message = NEGATIVE_SIZE_ERROR.format(value=negative_size)
    with pytest.raises(ValueError, match=expected_message):
        validate_params(**params)


@pytest.mark.parametrize('distance_exceedance', [
    MINIMAL_TEST_VALUE,
    1,
    10000
])
def test_big_distance_with_fragile_raises_exception(default_params, distance_exceedance) -> None:
    exceed_distance = MAX_FRAGILE_DISTANCE + distance_exceedance
    params = {**default_params, 'fragile': True, 'distance': exceed_distance}

    expected_message = DISTANCE_EXCEED_WITH_FRAGILE_ERROR.format(
        value=exceed_distance, max_distance=MAX_FRAGILE_DISTANCE
    )
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
        DISTANCE_EXCEED_WITH_FRAGILE_ERROR.format(value=exceed_distance, max_distance=MAX_FRAGILE_DISTANCE),
    ]
    with pytest.raises(ValueError) as exc_info:
        validate_params(**params)

    exception_full_text = str(exc_info.value)
    for expected_message in expected_messages:
        assert (
                expected_message in exception_full_text
        ), f'Expected error "{exception_full_text}"\nnot found in: "{exception_full_text}"'
