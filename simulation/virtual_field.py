"""A one-dimensional field with known weed positions, for timing tests."""
def make_field(target_positions_m=None):
    return [{"target_id": i + 1, "position_m": float(x), "lateral_m": 0.0,
             "class_name": "weed", "confidence": 0.90}
            for i, x in enumerate(target_positions_m or [3.0, 5.5, 8.0, 10.0])]
