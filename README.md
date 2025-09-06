# dummysensors

[![PyPI version](https://img.shields.io/pypi/v/dummysensors.svg)](https://pypi.org/project/dummysensors/)
[![CI](https://github.com/SculptTechProject/dummysensors/actions/workflows/ci.yml/badge.svg)](https://github.com/SculptTechProject/dummysensors/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight generator of dummy sensor data for IoT and ML testing.
Provides a simple Python API and CLI, supports running multiple sensors in parallel, photovoltaic domain sensors, and splitting output streams into files.

---

## Installation

From PyPI (recommended):

```bash
pip install dummysensors
```

---

## Quick Start (API)

```python
from dummysensors import TemperatureSensor, VibrationSensor

# create sensors
temp = TemperatureSensor(min_val=18, max_val=24, noise=0.2)
vib  = VibrationSensor(base_hz=50.0, amp=1.0, noise=0.05)

print(temp.read())            # e.g. 21.3
print(vib.read(t_s=0.123))    # sinusoidal signal with noise
```

---

## Config file (YAML)

Instead of passing long `--spec` strings, you can define your setup in a YAML file.
By default, `dummy-sensors run --config config.sensors.yaml` will look for a file named `config.sensors.yaml` in the current directory.

### Example `config.sensors.yaml`

```yaml
rate: 2
count: 5
partition_by: type

outputs:
  - type: jsonl
    for: temp
    path: out/temp.jsonl
  - type: csv
    for: vibration
    path: out/vibration.csv

devices:
  - id: engine-A
    sensors:
      - kind: temp
        count: 1
      - kind: vibration
        count: 1
  - id: plant-1
    sensors:
      - kind: irradiance
        count: 1
        params: {peak: 900.0, day_period_s: 10.0, sunrise: 0.0, sunset: 10.0}
      - kind: pv_power
        count: 1
        params: {stc_kw: 5.0, inverter_eff: 0.95, p_kw_max: 4.8}
      - kind: load
        count: 1
        params: {base_kw: 0.3, morning_kw: 0.8, evening_kw: 1.2}
      - kind: soc
        count: 1
        params: {capacity_kwh: 10.0, soc0: 50.0}
```

Run with:

```bash
dummy-sensors run --config config.sensors.yaml
```

---

## Quick Start (CLI)

Generate a single temperature stream to JSONL:

```bash
dummy-sensors generate --rate 5 --duration 2 --jsonl out/temp.jsonl
```

Run multiple sensors and devices, split by **type** into separate files:

```bash
dummy-sensors run \
  --rate 5 \
  --count 30 \
  --spec "device=engine-A: temp*1,vibration*2; device=room-101: temp*2" \
  --out "temp=out/temp.jsonl" \
  --out "vibration=out/vib.jsonl" \
  --out "*=stdout"
```

> 👉 Check out a full demo with live plotting and JSONL logging here:
> [dummysensors demo (ds-test)](https://github.com/SculptTechProject/ds-test)

---

## `--spec` format

The `--spec` string describes devices and sensors:

```
device=<ID>: <type>*<count>[, <type>*<count> ...] ; device=<ID2>: ...
```

Examples:

* `device=A: temp*3` — device A with three temperature sensors
* `device=eng: temp*1,vibration*2; device=room: temp*2`

> As of `v0.3`, supported sensor types:
> `temp`, `vibration`, `irradiance`, `pv_power`, `load`, `soc`.
> You can define setups either with `--spec` (quick inline config) or using a YAML file (`--config config.sensors.yaml`) for more complex scenarios.

---

## Python API

Below is the up‑to‑date API that matches the code. All times are in seconds; pass monotonic time to `t_s` for stable integration. If `t_s=None`, sensors start from 0.

### `TemperatureSensor`

Daily temperature: sine wave + OU noise.

**Parameters (defaults):**

* `min_val: float = 15.0`
* `max_val: float = 30.0`
* `period_s: float = 24*3600`
* `phase_shift: float = -4*3600` — shift so the maximum is in the evening
* `noise_theta: float = 0.05` — mean‑reversion strength in OU
* `noise_sigma: float = 0.3` — OU noise scale

**Methods:**

* `read(t_s: float | None = None) -> float` — temperature in °C

---

### `VibrationSensor`

Base sine at `base_hz` + OU noise + rare spikes.

**Parameters (defaults):**

* `base_hz: float = 50.0`
* `amp: float = 1.0`
* `noise_theta: float = 2.0`
* `noise_sigma: float = 0.05`
* `spike_prob: float = 0.001` — spike probability per sample
* `spike_scale: float = 4.0` — spike magnitude (× `amp`)

**Methods:**

* `read(t_s: float | None = None) -> float`

---

### `IrradianceSensor`

Solar irradiance (W/m²): half‑sine between sunrise and sunset + slow OU “clouds”.

**Parameters (defaults):**

* `peak: float = 900.0` — peak W/m²
* `day_period_s: float = 24*3600`
* `sunrise: float = 6*3600`
* `sunset: float = 18*3600`
* `cloud_theta: float = 1/600.0` — slow cloud dynamics
* `cloud_sigma: float = 0.05`

**Methods:**

* `read(t_s: float | None = None) -> float` — W/m² (>= 0)

Note: the cloud factor is clamped to 0.2–1.2.

---

### `PVPowerSensor`

Inverter AC power (kW). Model:
`P_dc ≈ (irradiance/1000) * stc_kw`,
`P_ac = min(p_kw_max, max(0, P_dc * inverter_eff)) + N(0, noise_sigma)`

**Parameters (defaults):**

* `stc_kw: float = 5.0` — STC power at 1000 W/m²
* `inverter_eff: float = 0.95`
* `p_kw_max: float = 4.8`
* `noise_sigma: float = 0.05`

**Methods:**

* `read(t_s: float | None = None, irradiance: float | None = None) -> float`

  * Returns `0.0` if `irradiance is None`.

---

### `LoadSensor`

Consumption (kW): base + two daily “bumps” (morning & evening) + OU.

**Parameters (defaults):**

* `base_kw: float = 0.5`
* `morning_kw: float = 0.8`
* `evening_kw: float = 1.2`
* `day_period_s: float = 24*3600`
* `noise_theta: float = 1/120.0`
* `noise_sigma: float = 0.05`

**Methods:**

* `read(t_s: float | None = None) -> float` — kW (>= 0)

---

### `BatterySoCSensor`

State‑of‑charge simulator (%), integrating the power balance. Sign convention: positive `net_power_kw` means an energy deficit → discharge; negative means surplus → charge. Power limits and efficiencies are respected.

**Parameters (defaults):**

* `capacity_kwh: float = 10.0`
* `soc0: float = 50.0` — initial SoC \[%]
* `charge_eff: float = 0.95`
* `discharge_eff: float = 0.95`
* `p_charge_max_kw: float = 3.0`
* `p_discharge_max_kw: float = 3.0`

**Methods:**

* `step(t_s: float, net_power_kw: float) -> float` — returns current SoC \[%]

> Note: this is **not** a `read()`. Call `step(...)` each tick with the power balance.

---

### Sensor dependencies

* `PVPowerSensor` needs `irradiance` (e.g., from `IrradianceSensor`).
* `BatterySoCSensor` needs `net_power_kw = load_kw - pv_kw` (or a general balance).
  Positive → discharge, negative → charge.

---

### Sensor Registry

* `dummysensors.registry.SENSOR_REGISTRY` — maps string `kind` → class
* `dummysensors.registry.make_sensor(kind: str, **params)` — construct by name

---

### Orchestrator

`dummysensors.orchestrator.run_stream(...)`

* Builds instances from a `spec_str` or a `config`.
* Respects sensor **priority** and per‑sensor `rate_hz`.
* `writer_for_type` is a map `type → callable(sample_dict)`, with `"*"` as the default writer.

---

### Implementation notes

* **OU (Ornstein–Uhlenbeck)** uses `dt` from successive calls; a tiny minimum `dt` is applied when time does not advance.
* Prefer passing monotonic time to `t_s` (e.g., `time.monotonic()`), especially when chaining sensors in a pipeline.

## Output Format

JSON Lines (one record per line):

```json
{
  "ts_ms": 171234,
  "device_id": "engine-A",
  "sensor_id": "vibration-1",
  "type": "vibration",
  "value": -0.124
}
```

Also supported: **CSV**. Planned: Kafka, Redis Stream, WebSocket.

---

## Roadmap

* `v0.2` ✅ — CSV writer, partitioning, YAML config
* `v0.3` ✅ — Smart photovoltaic sensors (`irradiance`, `pv_power`, `load`, `soc`), per-sensor `rate_hz`, priority-based orchestration
* `v0.4` 🚧 — AnomalyInjector (spike, dropout, drift), new sensors (`humidity`, `rpm`, `battery_voltage`, `gps`, `accel-3axis`)
* `v0.5` 🚧 — Outputs: Kafka, Redis Stream, WebSocket live preview

---

## Development

```bash
git clone https://github.com/SculptTechProject/dummysensors
cd dummysensors
pip install -e .
pip install -r requirements.txt
```

* Project layout: **src-layout**
* Tests: `pytest -q`
* Lint/format: `ruff check src tests` and `ruff format`

---

## License

MIT © Mateusz Dalke
