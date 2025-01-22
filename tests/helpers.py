MINIMAL_TEST_VALUE = 1e-6

def generate_boundaries_from_interval(value_cost_interval: dict[int, int]):
    lower_boundaries = [
        (float(distance), cost)
        for distance, cost in value_cost_interval.items()]
    upper_boundaries = [
        (upper_distance - MINIMAL_TEST_VALUE, cost)
        for upper_distance, cost in zip(list(value_cost_interval.keys())[1:], value_cost_interval.values())
    ]
    return lower_boundaries + upper_boundaries