from dummysensors import TemperatureSensor

def test_range():
    s = TemperatureSensor(10, 20, 0.1)
    vals = [s.read() for _ in range(100)]
    assert min(vals) > 8 and max(vals) < 22
