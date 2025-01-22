from .Workload import Workload

MAX_FRAGILE_DISTANCE = 30

INITIAL_COST = 0.
MINIMAL_COST = 400.

DISTANCE_COSTS: dict[int, int] = {
    0: 50,
    2: 100,
    10: 200,
    30: 300
}

SIZE_COSTS: dict[int, int]= {
    0: 100,
    2: 200  # exemplary BIG size
}

FRAGILE_COSTS: dict[bool, int] = {
    True: 300,
    False: 0
}

WORKLOAD_MULTIPLIERS: dict[Workload, float] = {
    Workload.VERY_HIGH: 1.6,
    Workload.HIGH: 1.4,
    Workload.MODERATE: 1.2,
    'DEFAULT': 1.
}
