from dummysensors import VibrationSensor
def test_vibration_basic():
    s = VibrationSensor(base_hz=10.0, amp=1.0, noise=0.0)
    xs = [s.read(t_s=i*0.01) for i in range(100)]
    assert max(xs) <= 1.0 + 1e-9 and min(xs) >= -1.0 - 1e-9
