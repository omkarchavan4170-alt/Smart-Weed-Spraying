"""Simple configurable image-to-ground mapping for a flat virtual field.
This is a simulation mapping, not camera calibration for a real machine.
"""
def pixel_to_ground(x_px, y_px, image_width, image_height, field_width_m=2.0, field_length_m=3.0):
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image dimensions must be positive")
    x_m = (x_px / image_width - 0.5) * field_width_m
    y_m = (1.0 - y_px / image_height) * field_length_m
    return x_m, y_m
