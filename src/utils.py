from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_config(path=None):
    path = Path(path) if path else ROOT / "config.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_parent(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
