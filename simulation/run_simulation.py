"""Run a deterministic, hardware-free timing and nozzle simulation."""
from pathlib import Path
import pandas as pd
from src.timing_engine import calculate_timing
from src.utils import ROOT, load_config
from simulation.virtual_field import make_field

def main():
    cfg = load_config()
    field = make_field()
    speed = float(cfg["vehicle_speed_mps"])
    distance = float(cfg["camera_nozzle_distance_m"])
    latency = sum(float(cfg[k]) for k in [
        "inference_latency_ms", "processing_latency_ms",
        "control_latency_ms", "nozzle_latency_ms"
    ])
    timing_rows, spray_rows = [], []
    for target in field:
        timing = calculate_timing(distance, speed, latency)
        activation_s = timing["remaining_wait_s"]
        # The demo assumes each target is detected when it is at the same
        # configured camera-relative distance. This isolates timing behavior.
        timing_rows.append({
            "scenario_id": target["target_id"], "speed_mps": speed,
            "distance_m": distance,
            "travel_time_ms": timing["travel_time_s"] * 1000,
            "latency_ms": latency,
            "remaining_wait_ms": timing["remaining_wait_s"] * 1000,
            "late_target": timing["late_target"],
        })
        spray_rows.append({
            "event_id": target["target_id"], "scenario_id": target["target_id"],
            "target_id": target["target_id"], "activation_time_s": activation_s,
            "confidence": target["confidence"],
            "spray_duration_s": 0.4,
            "hit": not timing["late_target"], "late": timing["late_target"]
        })
    (ROOT / "logs").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(timing_rows).to_csv(ROOT / "logs/timing_log.csv", index=False)
    pd.DataFrame(spray_rows).to_csv(ROOT / "logs/spray_log.csv", index=False)
    print("Software-only simulation complete.")
    print(f"Speed={speed:.2f} m/s | camera-nozzle distance={distance:.2f} m")
    print(f"Total modeled latency={latency:.1f} ms")
    print(f"Travel time={distance/speed*1000:.1f} ms")
    print(f"Late target={latency >= distance/speed*1000}")
    print("Logs written to logs/timing_log.csv and logs/spray_log.csv")
    print("Note: this is a timing demonstration; target positions are synthetic.")

if __name__ == "__main__":
    main()
