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

[0.1.0]: https://github.com/SculptTechProject/dummysensors/releases/tag/v0.1.0

