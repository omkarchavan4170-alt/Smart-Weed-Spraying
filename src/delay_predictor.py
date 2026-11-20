from pathlib import Path
import joblib
import pandas as pd
from src.utils import ROOT

def predict_latency_ms(features, model_path=None):
    path = Path(model_path) if model_path else ROOT / "models/delay_regressor.pkl"
    if not path.exists():
        raise FileNotFoundError(f"Delay model missing: {path}. Run python -m src.train_delay_model")
    bundle = joblib.load(path)
    row = pd.DataFrame([features], columns=bundle["features"])
    return float(bundle["model"].predict(row)[0])
