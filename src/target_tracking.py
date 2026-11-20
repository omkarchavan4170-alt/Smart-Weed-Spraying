"""Minimal target de-duplication by proximity for replay prototypes."""
import math

class TargetTracker:
    def __init__(self, distance_threshold_px=40):
        self.distance_threshold_px = distance_threshold_px
        self.targets = []
        self.next_id = 1

    def update(self, detections):
        # Each detection: dict with x_center, y_center, confidence, class_name
        output = []
        for det in detections:
            match = None
            for target in self.targets:
                d = math.hypot(det["x_center"] - target["x_center"],
                               det["y_center"] - target["y_center"])
                if d <= self.distance_threshold_px:
                    match = target
                    break
            if match is None:
                match = {"target_id": self.next_id}
                self.next_id += 1
                self.targets.append(match)
            match.update(det)
            output.append({**match})
        return output
