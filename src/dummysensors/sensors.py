import random, math
from dataclasses import dataclass

@dataclass
class TemperatureSensor:
    def __init__(self, min_val=15, max_val=30, noise=0.5):
        self.min_val = min_val
        self.max_val = max_val
        self.noise = noise

    def read(self):
        base = random.uniform(self.min_val, self.max_val)
        return base + random.gauss(0, self.noise)

@dataclass
class VibrationSensor:
    type: str = "vibration"
    base_hz: float = 50.0
    amp: float = 1.0
    noise: float = 0.1
    spike_prob: float = 0.0  # for tests 0

    def read(self, t_s: float | None = None) -> float:
        t_s = 0.0 if t_s is None else t_s
        sig = self.amp * math.sin(2 * math.pi * self.base_hz * t_s)
        sig += random.gauss(0, self.noise)
        return sig
