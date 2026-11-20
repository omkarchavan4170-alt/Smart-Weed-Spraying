"""YOLO training wrapper. Requires a labeled dataset configured in data/data.yaml."""
from pathlib import Path
from ultralytics import YOLO
from src.utils import ROOT, load_config

def main():
    data_yaml = ROOT / "data/data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError(data_yaml)
    model = YOLO("yolov8n.pt")
    model.train(data=str(data_yaml), imgsz=640, epochs=50, batch=8, project=str(ROOT / "outputs"), name="weed_train")
    best = ROOT / "outputs/weed_train/weights/best.pt"
    if best.exists():
        destination = ROOT / "models/weed_detector.pt"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(best.read_bytes())
        print(f"Copied trained weights to {destination}")
    else:
        print("Training finished but best.pt was not found at the expected path.")

if __name__ == "__main__":
    main()
