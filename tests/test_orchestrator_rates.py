from __future__ import annotations
from dummysensors.orchestrator import run_stream
from .utils import Capture

def test_per_sensor_rate_hz_controls_sampling_frequency():
    cap = Capture()
    devices_cfg = [{
        "id": "A",
        "sensors": [
            {"kind": "temp",      "count": 1, "priority": 5, "rate_hz": 5},   # every 0.2s
            {"kind": "vibration", "count": 1, "priority": 5, "rate_hz": 10},  # every 0.1s
        ]
    }]

    run_stream(
        spec_str="device=A: temp*1,vibration*1",
        rate_hz=10.0,              # global tick
        duration_s=None,
        total_count=20,            # ~2.0s
        writer_for_type={"*": cap.router({"*": cap.writer_for_type("*")})},
        partition_by="none",
        devices_cfg=devices_cfg,
    )

    n_temp = len([r for r in cap.per_type["*"] if r["type"] == "temp"]) \
             if "*" in cap.per_type else len([r for r in cap.per_type.get("temp", [])])
    n_vib  = len([r for r in cap.per_type["*"] if r["type"] == "vibration"]) \
             if "*" in cap.per_type else len([r for r in cap.per_type.get("vibration", [])])

    # vibration should have noticeably more samples than temp (timing tolerance)
    assert n_vib >= n_temp + 5, f"expected more vib samples than temp; got temp={n_temp}, vib={n_vib}"
