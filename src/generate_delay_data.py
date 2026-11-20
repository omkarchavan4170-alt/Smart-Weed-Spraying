"""Generate reproducible synthetic timing scenarios. Values are simulated, not hardware measurements."""
from pathlib import Path
import numpy as np
import pandas as pd
from src.utils import ROOT

def generate(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    speed = rng.uniform(0.4, 3.5, n)
    distance = rng.uniform(0.4, 2.0, n)
    inference = np.clip(rng.normal(80, 25, n), 20, 180)
    processing = np.clip(rng.normal(45, 20, n), 5, 130)
    control = np.clip(rng.normal(20, 8, n), 2, 60)
    nozzle = np.clip(rng.normal(25, 7, n), 5, 60)
    lateral = rng.uniform(-0.5, 0.5, n)
    # Simulated total latency has a small position/load-dependent component and noise.
    total = inference + processing + control + nozzle + 0.02 * np.abs(lateral) * 1000
    total += rng.normal(0, 5, n)
    total = np.clip(total, 1, None)
    df = pd.DataFrame({
        "speed_mps": speed,
        "camera_nozzle_distance_m": distance,
        "inference_ms": inference,
        "processing_ms": processing,
        "control_ms": control,
        "nozzle_ms": nozzle,
        "target_lateral_m": lateral,
        "latency_ms": total,
    })
    out = ROOT / "data/synthetic/delay_training.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    scenarios = df.copy()
    scenarios.insert(0, "scenario_id", np.arange(len(df)))
    scenarios["distance_m"] = scenarios["camera_nozzle_distance_m"]
    scenarios["seed"] = seed
    scenarios.to_csv(ROOT / "data/synthetic/scenarios.csv", index=False)
    print(f"Saved {len(df)} synthetic rows to {out}")
    print("WARNING: labels are synthetic and do not represent real hardware measurements.")

if __name__ == "__main__":
    generate()
