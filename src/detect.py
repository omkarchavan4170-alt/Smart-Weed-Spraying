from pathlib import Path
import time
import cv2
from src.utils import ROOT, load_config

def detect_image(image_path, model_path=None, confidence=None):
    from ultralytics import YOLO
    cfg = load_config()
    model_path = Path(model_path or (ROOT / cfg["model_path"]))
    if not model_path.exists():
        raise FileNotFoundError(
            f"Weed detector not found at {model_path}. Train it first or use synthetic simulation."
        )
    model = YOLO(str(model_path))
    start = time.perf_counter()
    results = model.predict(
        source=str(image_path),
        conf=confidence if confidence is not None else cfg["confidence_threshold"],
        verbose=False
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    result = results[0]
    names = result.names
    detections = []
    if result.boxes is not None:
        for box in result.boxes:
            xyxy = box.xyxy[0].cpu().numpy().tolist()
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = xyxy
            detections.append({
                "class_id": cls_id, "class_name": names[cls_id],
                "confidence": conf, "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "x_center": (x1+x2)/2, "y_center": (y1+y2)/2
            })
    return detections, elapsed_ms, result.plot()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    args = parser.parse_args()
    dets, ms, annotated = detect_image(args.image)
    out = ROOT / "outputs/detections"
    out.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out / "annotated.jpg"), annotated)
    print(f"Found {len(dets)} objects in {ms:.1f} ms")
