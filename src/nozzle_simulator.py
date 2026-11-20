class NozzleSimulator:
    def __init__(self):
        self.is_on = False
        self.events = []

    def activate(self, time_s, target_id, confidence, duration_s, late=False):
        self.is_on = True
        event = {
            "event_id": len(self.events) + 1,
            "target_id": target_id,
            "activation_time_s": float(time_s),
            "confidence": float(confidence),
            "spray_duration_s": float(duration_s),
            "hit": not late,
            "late": bool(late),
        }
        self.events.append(event)
        self.is_on = False
        return event
