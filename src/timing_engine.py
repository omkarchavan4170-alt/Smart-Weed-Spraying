"""Physics timing and late-target handling."""
def calculate_timing(distance_m, speed_mps, elapsed_latency_ms):
    if distance_m <= 0:
        raise ValueError("distance_m must be positive")
    if speed_mps <= 0:
        raise ValueError("speed_mps must be positive")
    travel_s = distance_m / speed_mps
    latency_s = max(0.0, elapsed_latency_ms / 1000.0)
    remaining_s = max(0.0, travel_s - latency_s)
    late = latency_s >= travel_s
    return {
        "travel_time_s": travel_s,
        "elapsed_latency_s": latency_s,
        "remaining_wait_s": remaining_s,
        "late_target": late,
    }

def corrected_wait_s(distance_m, speed_mps, elapsed_latency_ms, correction_ms=0.0):
    result = calculate_timing(distance_m, speed_mps, elapsed_latency_ms)
    if result["late_target"]:
        return 0.0, True
    wait = max(0.0, result["remaining_wait_s"] + correction_ms / 1000.0)
    return wait, False
