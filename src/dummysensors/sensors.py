import random

class TemperatureSensor:
    def __init__(self, min_val=15, max_val=30, noise=0.5):
        self.min_val = min_val
        self.max_val = max_val
        self.noise = noise

    def read(self):
        base = random.uniform(self.min_val, self.max_val)
        return base + random.gauss(0, self.noise)
