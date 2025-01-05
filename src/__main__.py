from src.Workload import Workload
from src.config import DISTANCE_COSTS, WORKLOAD_MULTIPLIERS, SIZE_COSTS, FRAGILE_COSTS, MAX_FRAGILE_DISTANCE

INITIAL_COST = 0.
MINIMAL_COST = 400.


def calculate_delivery_cost(distance: float, size: float, fragile: bool, workload: Workload) -> float:
    errors = []
    if distance <= 0:
        errors.append(f'Distance should be positive, got {distance}')
    if size <= 0:
        errors.append(f'Size should be positive, got {size}')
    if not is_possible_to_deliver(fragile, distance):
        errors.append(f'Impossible to deliver fragile at distance {distance},'
                      f'should not be higher than {MAX_FRAGILE_DISTANCE})')
    if errors:
        raise ValueError('. '.join(errors))

    distance_cost = calculate_distance_cost(distance)
    size_cost = calculate_size_cost(size)
    fragile_cost = calculate_fragile_cost(fragile)
    workload_multiplier = calculate_workload_multiplier(workload)

    total_cost = (INITIAL_COST + distance_cost + size_cost + fragile_cost) * workload_multiplier
    return (total_cost if total_cost >= MINIMAL_COST
            else MINIMAL_COST)


def is_possible_to_deliver(fragile: bool, distance: float) -> bool:
    return (not fragile
            or distance <= MAX_FRAGILE_DISTANCE)


def calculate_distance_cost(distance: float) -> int:
    return next(cost
                for limit, cost in DISTANCE_COSTS.items()
                if distance >= limit)


def calculate_size_cost(size: float) -> int:
    return next(cost
                for limit, cost in SIZE_COSTS.items()
                if size >= limit)


def calculate_fragile_cost(fragile: bool) -> int:
    return FRAGILE_COSTS[fragile]


def calculate_workload_multiplier(workload: Workload) -> float:
    default_multiplier = WORKLOAD_MULTIPLIERS['DEFAULT']
    return WORKLOAD_MULTIPLIERS.get(workload, default_multiplier)
