class VehicleSimulator:
    def __init__(self, speed_mps=2.0, position_m=0.0):
        self.speed_mps = float(speed_mps)
        self.position_m = float(position_m)
        if self.speed_mps < 0:
            raise ValueError("speed_mps cannot be negative")

    def step(self, dt_s):
        self.position_m += self.speed_mps * dt_s
        return self.position_m
