from __future__ import annotations
import argparse, json, time, sys, csv
from .sensors import TemperatureSensor

def _stdout_writer():
    def _w(sample: dict):
        sys.stdout.write(json.dumps(sample) + "\n")
    return _w

def _jsonl_file_writer(path: str):
    f = open(path, "a", buffering=1, encoding="utf-8")
    def _w(sample: dict):
        f.write(json.dumps(sample) + "\n")
    return _w

def main(argv=None):
    p = argparse.ArgumentParser(prog="dummy-sensors", description="Generate dummy sensor data")
    g = p.add_argument_group("generation")
    g.add_argument("--rate", type=float, default=5.0, help="Hz (samples per second)")
    g.add_argument("--duration", type=float, default=5.0, help="seconds")
    g.add_argument("--count", type=int, default=None, help="override number of samples")
    g.add_argument("--min", dest="min_val", type=float, default=15.0)
    g.add_argument("--max", dest="max_val", type=float, default=30.0)
    g.add_argument("--noise", type=float, default=0.5)

    o = p.add_argument_group("output")
    o.add_argument("--jsonl", type=str, default=None, help="path to JSONL file; if omitted prints to stdout")

    args = p.parse_args(argv)

    # writer
    writer = _jsonl_file_writer(args.jsonl) if args.jsonl else _stdout_writer()

    # sensor (temp)
    s = TemperatureSensor(min_val=args.min_val, max_val=args.max_val, noise=args.noise)

    # main loop
    period = 1.0 / args.rate if args.rate > 0 else 0.0
    total = args.count if args.count is not None else int(args.duration * args.rate)

    t0 = time.perf_counter()
    for i in range(total):
        t_s = time.perf_counter() - t0
        val = s.read()
        writer({"ts_ms": int(t_s * 1000), "device_id": "dev-0", "sensor_id": "temp-0", "type": "temp", "value": float(val)})
        if period > 0:
            # simple busy wait
            t_next = t0 + (i + 1) * period
            while time.perf_counter() < t_next:
                time.sleep(min(0.002, t_next - time.perf_counter()))

if __name__ == "__main__":
    main()
