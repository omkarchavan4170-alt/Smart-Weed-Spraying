from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.utils import ROOT

def timing_metrics(actual_ms, predicted_ms):
    actual = np.asarray(actual_ms, dtype=float)
    pred = np.asarray(predicted_ms, dtype=float)
    return {
        "mae_ms": float(mean_absolute_error(actual, pred)),
        "rmse_ms": float(np.sqrt(mean_squared_error(actual, pred))),
    }

def evaluate_timing_csv(path=None):
    path = Path(path) if path else ROOT / "data/synthetic/delay_training.csv"
    df = pd.read_csv(path)
    print(df.describe())
    return df.describe()

if __name__ == "__main__":
    evaluate_timing_csv()
