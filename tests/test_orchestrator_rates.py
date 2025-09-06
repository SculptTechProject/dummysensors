from __future__ import annotations
from dummysensors.orchestrator import run_stream
from .utils import Capture

def test_per_sensor_rate_hz_controls_sampling_frequency():
    cap = Capture()
    devices_cfg = [{
        "id": "A",
        "sensors": [
            {"kind": "temp",      "count": 1, "priority": 5, "rate_hz": 5},   # ~every 0.2s
            {"kind": "vibration", "count": 1, "priority": 5, "rate_hz": 10},  # ~every 0.1s
        ]
    }]

    run_stream(
        spec_str="device=A: temp*1,vibration*1",
        rate_hz=10.0,                 # global tick
        duration_s=None,
        total_count=20,               # ~2.0s
        writer_for_type={"*": cap.router({"*": cap.writer_for_type("*")})},
        partition_by="none",
        devices_cfg=devices_cfg,
    )

    # Count how many samples we collected for each type
    all_recs = cap.per_type.get("*")
    if all_recs is not None:
        n_temp = sum(1 for r in all_recs if r["type"] == "temp")
        n_vib  = sum(1 for r in all_recs if r["type"] == "vibration")
    else:
        n_temp = len(cap.per_type.get("temp", []))
        n_vib  = len(cap.per_type.get("vibration", []))

    # Expect significantly more vibration samples (10 Hz) than temperature (5 Hz).
    # Leave tolerance for CI timing jitter: require at least 1.5× more vib or +3 samples.
    assert n_vib >= max(int(1.5 * n_temp), n_temp + 3), \
        f"expected clearly more vib samples than temp; got temp={n_temp}, vib={n_vib}"
