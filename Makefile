SHELL := /usr/bin/env bash
PY := .venv/Scripts/python.exe
PIP := .venv/Scripts/pip.exe

.PHONY: venv install test clean demo demo-clean

venv:
	@if [ ! -d .venv ]; then python -m venv .venv; fi
	@$(PIP) -q install -U pip

install: venv
	@$(PIP) -q install -e .
	@echo "✔ Installed dummysensors in editable mode"

test:
	@$(PY) -m pytest -q

clean:
	@rm -rf build dist *.egg-info .pytest_cache
	@find . -name "__pycache__" -type d -prune -exec rm -rf {} +

demo-clean:
	@rm -rf out demo_out

# DEMO: 2 types of sensors, 2 devices, 3 outputs (2 files + stdout)
demo: install
	@mkdir -p demo_out
	@dummy-sensors run --rate 5 --count 30 \
	  --spec "device=engine-A: temp*1,vibration*2; device=room-101: temp*2" \
	  --out "temp=demo_out/temp.jsonl" \
	  --out "vibration=demo_out/vibration.jsonl" \
	  --out "*=stdout"
	@echo "✔ Demo done. Files in demo_out/"
