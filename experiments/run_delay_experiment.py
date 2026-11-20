from pathlib import Path
import itertools
import pandas as pd
from src.timing_engine import calculate_timing
from src.utils import ROOT

def main():
    rows = []
    for speed, distance, latency in itertools.product(
        [0.5, 1.0, 2.0, 3.0], [0.5, 1.0, 1.5], [20, 80, 150, 250, 350]
    ):
        result = calculate_timing(distance, speed, latency)
        rows.append({
            "speed_mps": speed, "distance_m": distance,
            "latency_ms": latency, "travel_time_ms": result["travel_time_s"]*1000,
            "remaining_wait_ms": result["remaining_wait_s"]*1000,
            "late_target": result["late_target"]
        })
    out = ROOT / "outputs/reports/delay_experiment.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"Saved {len(rows)} scenarios to {out}")

if __name__ == "__main__":
    main()
