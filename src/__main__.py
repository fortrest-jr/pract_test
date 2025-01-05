from src.Workload import Workload

INITIAL_COST = 0
BIG_SIZE = 2


def calculate_delivery_cost(distance: float, size: float, fragile: bool, workload: Workload) -> float:
    if not is_possible_to_deliver(fragile, distance):
        raise ValueError(f'Impossible to deliver fragile at distance {distance} (should not be higher than 30)')

    return ((calculate_distance_cost(distance)
             + calculate_size_cost(size)
             + calculate_fragile_cost(fragile))
            * calculate_workload_multiplier(workload))


def calculate_distance_cost(distance: float) -> int:
    if distance < 2:
        return 50
    elif distance < 10:
        return 100
    elif distance < 30:
        return 200
    else:
        return 300


def calculate_size_cost(size: float) -> int:
    return (100 if size < BIG_SIZE
            else 200)


def is_possible_to_deliver(fragile: bool, distance: float) -> bool:
    return (not fragile
            or distance <= 30)


def calculate_fragile_cost(fragile: bool) -> int:
    return (300 if fragile
            else 0)


def calculate_workload_multiplier(workload: Workload) -> float:
    match workload:
        case Workload.VERY_HIGH:
            return 1.6
        case Workload.HIGH:
            return 1.4
        case Workload.MODERATE:
            return 1.2
        case _:
            return 1.


if __name__ == '__main__':
    calculate_delivery_cost(1.1, 1.1, True, Workload.MODERATE)
