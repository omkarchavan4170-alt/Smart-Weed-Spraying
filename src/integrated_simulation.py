
# src/integrated_simulation.py

import argparse
import csv
import time
from pathlib import Path

import cv2

from src.detect import detect_image
from src.delay_predictor import predict_latency_ms
from src.scheduler import Task, simulate_edf
from src.utils import ROOT, load_config


def save_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        print(f"No records to save: {path}")
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(
        description="YOLO weed detection with EDF spray-job scheduling"
    )
    parser.add_argument("--image", required=True)
    parser.add_argument("--conf", type=float, default=0.10)
    args = parser.parse_args()

    if not 0 <= args.conf <= 1:
        parser.error("--conf must be between 0 and 1")

    image_path = Path(args.image)
    if not image_path.is_absolute():
        image_path = ROOT / image_path

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    cfg = load_config()

    speed = float(cfg["vehicle_speed_mps"])
    distance = float(cfg["camera_nozzle_distance_m"])
    processing_ms = float(cfg["processing_latency_ms"])
    control_ms = float(cfg["control_latency_ms"])
    nozzle_ms = float(cfg["nozzle_latency_ms"])
    spray_duration_s = float(cfg["spray_duration_s"])

    if speed <= 0 or distance <= 0:
        raise ValueError("Vehicle speed and distance must be positive.")

    # Run detector.
    detector_start = time.perf_counter()
    detections, inference_ms, annotated = detect_image(
        str(image_path),
        confidence=args.conf,
    )
    detector_call_ms = (
        time.perf_counter() - detector_start
    ) * 1000

    output_dir = ROOT / "outputs" / "detections"
    output_dir.mkdir(parents=True, exist_ok=True)
    annotated_path = output_dir / "integrated_annotated.jpg"

    if annotated is not None:
        if not cv2.imwrite(str(annotated_path), annotated):
            raise OSError(f"Could not save {annotated_path}")

    print("\n========== DETECTION RESULTS ==========")
    print(f"Raw detections: {len(detections)}")
    print(f"Confidence threshold: {args.conf:.2f}")
    print(f"Reported inference time: {inference_ms:.2f} ms")
    print(f"Detector-call time: {detector_call_ms:.2f} ms")

    for det in detections:
        print(
            f"class={det.get('class_name')}, "
            f"id={det.get('class_id', 'unknown')}, "
            f"confidence={float(det.get('confidence', 0)):.3f}"
        )

    # Keep only detections classified as weeds.
    accepted = [
        det for det in detections
        if str(det.get("class_name", "")).strip().lower() == "weed"
        and float(det.get("confidence", 0)) >= args.conf
    ]

    print(f"Accepted weed targets: {len(accepted)}")

    # Generate jobs using the existing delay predictor.
    travel_time_ms = (distance / speed) * 1000
    tasks = []
    target_details = {}

    for index, det in enumerate(accepted, start=1):
        features = {
            "speed_mps": speed,
            "camera_nozzle_distance_m": distance,
            "inference_ms": float(inference_ms),
            "processing_ms": processing_ms,
            "control_ms": control_ms,
            "nozzle_ms": nozzle_ms,
            "target_lateral_m": 0.0,
        }

        predicted_ms = float(predict_latency_ms(features))

        if predicted_ms < 0:
            raise ValueError("Predicted latency cannot be negative.")

        task_id = f"Weed_{index}"

        # Simplified model: each weed job gets its own estimated
        # processing cost and deadline from camera-to-nozzle travel.
        tasks.append(
            Task(
                task_id=task_id,
                execution_ms=predicted_ms,
                deadline_ms=travel_time_ms,
                arrival_ms=0.0,
            )
        )

        target_details[task_id] = {
            "confidence": float(det.get("confidence", 0)),
            "predicted_latency_ms": predicted_ms,
        }

    # Run the actual EDF scheduler.
    result = simulate_edf(tasks)
    timing_rows = []
    spray_rows = []

    print("\n========== EDF SCHEDULE ==========")
    print(f"Scheduling policy: {result['policy']}")

    for job in result["schedule"]:
        target_id = job["task_id"]
        detail = target_details[target_id]
        missed = job["deadline_missed"]

        timing_rows.append({
            **job,
            "confidence": round(detail["confidence"], 3),
            "predicted_latency_ms": round(
                detail["predicted_latency_ms"], 2
            ),
            "vehicle_speed_mps": speed,
            "camera_nozzle_distance_m": distance,
        })

        spray_rows.append({
            "target_id": target_id,
            "confidence": round(detail["confidence"], 3),
            "scheduled_start_ms": job["start_ms"],
            "scheduled_finish_ms": job["finish_ms"],
            "deadline_ms": job["deadline_ms"],
            "spray_duration_s": spray_duration_s,
            "spray_scheduled": not missed,
            "deadline_missed": missed,
            "spray_hit": False,
            "note": (
                "Timing-only simulation; physical spray intersection "
                "and target ground position are not calibrated."
            ),
        })

        print(
            f"{target_id}: start={job['start_ms']:.1f} ms, "
            f"finish={job['finish_ms']:.1f} ms, "
            f"deadline={job['deadline_ms']:.1f} ms, "
            f"missed={missed}"
        )

    logs_dir = ROOT / "logs"
    save_csv(logs_dir / "integrated_timing.csv", timing_rows)
    save_csv(logs_dir / "integrated_spray.csv", spray_rows)

    print("\n========== SUMMARY ==========")
    print(f"Detected objects: {len(detections)}")
    print(f"Accepted weed targets: {len(accepted)}")
    print(f"Travel-time deadline: {travel_time_ms:.1f} ms")
    print(f"Scheduled jobs: {result['total_jobs']}")
    print(f"Deadline misses: {result['deadline_misses']}")

    print(
        "\nCaution: the delay predictor uses synthetic training data. "
        "This EDF simulation does not prove real-time performance. "
        "The detector-call time includes startup overhead, and the "
        "current model does not account for calibrated target positions."
    )


if __name__ == "__main__":
    main()
