class VirtualCamera:
    def __init__(self, capture_interval_s=0.1, camera_offset_m=1.5):
        self.capture_interval_s = capture_interval_s
        self.camera_offset_m = camera_offset_m
        self.frame_id = 0

    def capture(self, simulation_time_s, vehicle_position_m):
        self.frame_id += 1
        return {
            "frame_id": self.frame_id,
            "capture_time_s": simulation_time_s,
            "vehicle_position_m": vehicle_position_m,
            "camera_position_m": vehicle_position_m + self.camera_offset_m,
        }
