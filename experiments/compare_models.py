"""Compare a constant latency baseline with the trained regressor on held-out rows."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.utils import ROOT
from src.train_delay_model import FEATURES

def main():
    path = ROOT / "data/synthetic/delay_training.csv"
    df = pd.read_csv(path)
    _, test = train_test_split(df, test_size=0.2, random_state=42)
    baseline = np.full(len(test), df["latency_ms"].iloc[0])
    print("Constant baseline MAE:", mean_absolute_error(test["latency_ms"], baseline))
    model_path = ROOT / "models/delay_regressor.pkl"
    if not model_path.exists():
        print("Train first: python -m src.train_delay_model")
        return
    import joblib
    bundle = joblib.load(model_path)
    pred = bundle["model"].predict(test[FEATURES])
    print("RandomForest MAE:", mean_absolute_error(test["latency_ms"], pred))
    print("RandomForest RMSE:", np.sqrt(mean_squared_error(test["latency_ms"], pred)))

if __name__ == "__main__":
    main()
