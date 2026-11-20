from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from src.utils import ROOT

FEATURES = [
    "speed_mps", "camera_nozzle_distance_m", "inference_ms",
    "processing_ms", "control_ms", "nozzle_ms", "target_lateral_m"
]

def main():
    data_path = ROOT / "data/synthetic/delay_training.csv"
    if not data_path.exists() or data_path.stat().st_size == 0:
        from src.generate_delay_data import generate
        generate()
    df = pd.read_csv(data_path)
    X, y = df[FEATURES], df["latency_ms"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(
        n_estimators=200, min_samples_leaf=3, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Latency MAE: {mean_absolute_error(y_test, pred):.2f} ms")
    print(f"Latency RMSE: {np.sqrt(mean_squared_error(y_test, pred)):.2f} ms")
    out = ROOT / "models/delay_regressor.pkl"
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, out)
    print(f"Saved model: {out}")
    print("Interpret results as synthetic-data validation only.")

if __name__ == "__main__":
    main()
