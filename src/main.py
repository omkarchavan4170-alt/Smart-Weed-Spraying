import argparse
import cv2
from src.detect import detect_image
from src.utils import ROOT

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--conf", type=float, default=0.25)
    args = parser.parse_args()

    detections, inference_ms, annotated = detect_image(
        args.image, confidence=args.conf
    )

    out = ROOT / "outputs/detections"
    out.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out / "annotated.jpg"), annotated)

    print(f"Detections: {len(detections)}")
    print(f"Inference: {inference_ms:.1f} ms")
    for d in detections:
        print(d["class_name"], f'confidence={d["confidence"]:.3f}')

    print(f"Saved: {out / 'annotated.jpg'}")

if __name__ == "__main__":
    main()
