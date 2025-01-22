from bisect import bisect_right

from src.Workload import Workload
from src.Config import (
    DISTANCE_COSTS,
    WORKLOAD_MULTIPLIERS,
    SIZE_COSTS,
    FRAGILE_COSTS,
    MAX_FRAGILE_DISTANCE,
    INITIAL_COST,
    MINIMAL_COST,
)
from src.Errors import (
    NEGATIVE_DISTANCE_ERROR,
    NEGATIVE_SIZE_ERROR,
    DISTANCE_EXCEED_WITH_FRAGILE_ERROR,
    CANNOT_GET_VALUE_FROM_INTERVAL_ERROR,
)


def calculate_delivery_cost(distance: float, size: float, fragile: bool, workload: Workload) -> float:
    validate_params(distance, size, fragile)

    distance_cost = calculate_distance_cost(distance)
    size_cost = calculate_size_cost(size)
    fragile_cost = calculate_fragile_cost(fragile)
    workload_multiplier = calculate_workload_multiplier(workload)

    total_cost = (INITIAL_COST + distance_cost + size_cost + fragile_cost) * workload_multiplier
    return (total_cost if total_cost >= MINIMAL_COST
            else MINIMAL_COST)


def validate_params(distance: float, size: float, fragile: bool) -> None:
    errors = []
    if distance < 0:
        errors.append(NEGATIVE_DISTANCE_ERROR.format(value=distance))
    if size < 0:
        errors.append(NEGATIVE_SIZE_ERROR.format(value=size))
    if not is_possible_to_deliver(fragile, distance):
        errors.append(DISTANCE_EXCEED_WITH_FRAGILE_ERROR.format(value=distance, max_distance=MAX_FRAGILE_DISTANCE))
    if errors:
        raise ValueError('. '.join(errors))


def is_possible_to_deliver(fragile: bool, distance: float) -> bool:
    return (not fragile
            or distance <= MAX_FRAGILE_DISTANCE)


def calculate_distance_cost(distance: float) -> int:
    return get_cost_from_interval(DISTANCE_COSTS, distance, 'distance')


def calculate_size_cost(size: float) -> int:
    return get_cost_from_interval(SIZE_COSTS, size, 'size')


def calculate_fragile_cost(fragile: bool) -> int:
    return FRAGILE_COSTS[fragile]


def calculate_workload_multiplier(workload: Workload) -> float:
    default_multiplier = WORKLOAD_MULTIPLIERS['DEFAULT']
    return WORKLOAD_MULTIPLIERS.get(workload, default_multiplier)


def get_cost_from_interval(value_cost_interval: dict[int, int], param_value: float, param_name: str) -> int:
    param_vals = sorted(value_cost_interval.keys())
    current_val_idx = bisect_right(param_vals, param_value)
    if current_val_idx == 0:
        raise ValueError(CANNOT_GET_VALUE_FROM_INTERVAL_ERROR.format(
            param_name=param_name,
            param_value=param_value,
            lowest_value=param_vals[0]))
    current_val_start = param_vals[current_val_idx - 1]
    return value_cost_interval[current_val_start]
