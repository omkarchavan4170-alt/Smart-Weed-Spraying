from src.nozzle_simulator import NozzleSimulator

def duration_from_confidence(confidence):
    if confidence >= 0.85:
        return 0.70
    if confidence >= 0.70:
        return 0.40
    return 0.20

def simulate_spray_events(targets, activation_time_s=0.0, threshold=0.70, late_ids=None):
    nozzle = NozzleSimulator()
    late_ids = set(late_ids or [])
    for target in targets:
        confidence = float(target["confidence"])
        if confidence < threshold:
            continue
        nozzle.activate(
            time_s=activation_time_s,
            target_id=target.get("target_id", target.get("id", "unknown")),
            confidence=confidence,
            duration_s=duration_from_confidence(confidence),
            late=target.get("target_id", target.get("id")) in late_ids
        )
    return nozzle.events
