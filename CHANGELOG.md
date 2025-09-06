# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 04-09-2025

### Added

- Initial release of `dummysensors`
- `TemperatureSensor` with configurable range and noise
- `VibrationSensor` with sinusoidal signal and noise
- CLI with two commands:
  - `generate` for a single temperature stream
  - `run` for multi-device, multi-sensor streams
- Output to JSONL (stdout or files, partitioned by sensor type)
- Simple `--spec` string format to describe devices and sensors
- Basic test suite (pytest)
- CI/CD GitHub Actions (tests + lint + build + publish via Trusted Publishing)

## [0.2.0] - 2025-09-04

### Added

- CSV writer (header, line-buffering).
- `--partition-by device|type|none`.
- YAML config: `dummy-sensors run --config config.yaml`.
- Autodiscovery: `config.sensors.yaml` (preferred), also `dummysensors.yaml|yml`, `config.yaml|yml`.
- Tests: config discovery, CSV writer.

### Changed

- `publish.yml` stabilizowany pod Trusted Publishing.

## [0.3.0] - 2025-09-06



### Added

- PV/energy sensors: `irradiance`, `pv_power`, `load`, `soc`.
- Context-aware orchestration: per-tick device context (e.g. irradiance → pv_power → load → soc).
- Per-sensor `rate_hz` (optional) and `priority` (optional) in YAML.
- `params` block for sensors in YAML (tunable models: peaks, capacities, etc.).
- Tests: PV pipeline (day/night), SoC integration, per-sensor rate.

### Changed

- Orchestrator supports dependency order and per-sensor scheduling while remaining backward compatible with existing `--spec` and YAML without `params`.
- PV power noise can be configured; recommends `noise_sigma: 0.0` for strict night zeros.

### Fixed

- Minor pacing stability when sleeping to the next tick.

[0.3.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.3.0

[0.2.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.2.0

[0.1.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.1.0

