VENV := .venv
PY   := $(VENV)/bin/python

run: $(VENV)
	@$(PY) src/fly_in.py

debug: $(VENV)
	@$(PY) src/fly_in.py --debug

bench: $(VENV)
	@$(PY) src/fly_in.py --benchmark
	@echo "Benchmark results saved to bench.txt"

install $(VENV):
	@uv venv $(VENV)
	@uv pip install ursina pydantic flake8 mypy

lint: $(VENV)
	-@$(PY) -m flake8 src
	-@$(PY) -m mypy src --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)
	-@$(PY) -m flake8 src
	-@$(PY) -m mypy src --ignore-missing-imports --allow-subclassing-any --strict

clean:
	@rm -rf $(VENV)
	@find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -exec rm -rf {} +
	@rm -f out.txt bench.txt

.PHONY: run debug bench install lint lint-strict clean
