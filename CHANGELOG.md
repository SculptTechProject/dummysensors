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


## [0.2.0]https://github.com/SculptTechProject/dummysensors/releases/tag/v0.2.0 - 2025-09-04

### Added

- CSV writer (`--out "*.csv"`) z nagłówkiem i line-buffering.
- `--partition-by device|type|none` (routing do plików per device/type).
- YAML config: `dummy-sensors run --config config.yaml`.
- Autodiscovery configu: `config.sensors.yaml` (preferowane), plus `dummysensors.yaml|yml`, `config.yaml|yml`.
- Testy: config discovery, CSV writer.

### Changed

- `publish.yml` stabilizowany pod Trusted Publishing.


[0.2.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.2.0
[0.1.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.1.0
