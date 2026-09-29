# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A generative design tool for the *initial design phase* of a tiltrotor (VTOL) UAV. Given a set of aircraft constraints in `inputs.csv` (mass, span, airfoil coefficients, thickness ratio), it sweeps wingspan and cruise velocity to model drag, hover power, structural limits, and battery sizing, then reports the design that maximizes flight range and plots the trade-space.

The package name is `uav_design`. It models skin-friction, form, and induced drag; disk-loading hover power; FAA structural loading limits via Euler beam theory; taper/induced drag; and battery considerations for electric flight.

## Commands

Uses uv + a Taskfile (go-task). Python 3.12. Runtime deps in `[project.dependencies]`; dev tooling (pytest, ruff, mypy, pre-commit) in `[dependency-groups.dev]`.

```bash
task init                 # uv sync + install pre-commit hooks
task run                  # run the design sweep over inputs.csv and show plots
task format               # ruff format + ruff check --fix + mypy
task test                 # pytest with coverage over uav_design/
task ci                   # format + test (local CI mirror)
task clean                # remove .venv, caches, build artifacts
```

Run a single test:
```bash
uv run pytest tests/structures_test.py -v
```

## Layout

- `uav_design/` — the package.
  - `__main__.py` — the design sweep: reads `inputs.csv`, iterates over wingspan/velocity, computes the trade-space, prints the optimal aircraft details, and plots flight radius and hover time. Run with `python -m uav_design`.
  - `read_inputs.py` — parses `inputs.csv` into the constraint vector.
  - `aero_drag.py` — total, parasitic (skin-friction), and induced drag.
  - `hover.py` — hover power (disk loading) and take-off/landing energy.
  - `structures.py` — Euler beam theory: moments of area, point/uniform/triangle loads, torsion and bending strain.
  - `wing_calculations.py` — iterative wing-mass minimization against the strain limit.
  - `airfoil.py` — standalone NACA-style airfoil profile plot.
- `inputs.csv` — the aircraft constraints you edit to tailor a design.
- `tests/` — pytest suite mirroring the package modules.
