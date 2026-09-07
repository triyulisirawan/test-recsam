"""Pure physics engine. No Streamlit dependency."""

DISTANCE_FACTORS_TO_M = {"m": 1.0, "km": 1000.0, "cm": 0.01}
TIME_FACTORS_TO_S = {"s": 1.0, "min": 60.0, "h": 3600.0}

def speed(distance_m: float, time_s: float) -> float:
    if distance_m <= 0:
        raise ValueError("Distance must be greater than 0.")
    if time_s <= 0:
        raise ValueError("Time must be greater than 0.")
    return distance_m / time_s

def position(distance_m: float, total_time_s: float, elapsed_s: float) -> float:
    if distance_m < 0 or total_time_s <= 0 or elapsed_s < 0:
        raise ValueError("Invalid simulation values.")
    return min(distance_m, speed(distance_m, total_time_s) * elapsed_s)

def convert_distance_to_m(value: float, unit: str) -> float:
    return value * DISTANCE_FACTORS_TO_M[unit]

def convert_time_to_s(value: float, unit: str) -> float:
    return value * TIME_FACTORS_TO_S[unit]

def speed_in_units(mps: float, distance_unit: str, time_unit: str) -> float:
    return mps * TIME_FACTORS_TO_S[time_unit] / DISTANCE_FACTORS_TO_M[distance_unit]
