# mol-tdn

[![CI](https://github.com/danieleongari/mol-tdn/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleongari/mol-tdn/actions/workflows/ci.yaml)
[![Docs](https://github.com/danieleongari/mol-tdn/actions/workflows/docs.yaml/badge.svg)](https://danieleongari.github.io/mol-tdn/)
[![PyPI](https://img.shields.io/pypi/v/mol-tdn.svg)](https://pypi.org/project/mol-tdn/)
[![Python](https://img.shields.io/pypi/pyversions/mol-tdn.svg)](https://pypi.org/project/mol-tdn/)

`mol-tdn` is an explainable cubic-equation-of-state toolkit for pure molecular fluids. It targets molecular-simulation and adsorption researchers who need traceable fugacity, density, compressibility, residual-property, and model-comparison workflows.

> [!WARNING]
> This project is pre-alpha research software. Validate results independently before scientific, engineering, or safety-critical use.

## Why mol-tdn?

- Inspect every physical compressibility root and the selection reason.
- Compare van der Waals, RK, SRK, and Peng–Robinson models.
- Export temperature/pressure scans as tidy pandas tables.
- Create interactive Plotly or static Matplotlib figures through one API.
- Read and audit a deliberately compact pure-Python numerical core.

It is not intended to replace full property databases, process simulators, mixture flash packages, or reference-quality thermodynamic software. Read the [project manifesto](https://danieleongari.github.io/mol-tdn/manifesto/) and [ecosystem comparison](https://danieleongari.github.io/mol-tdn/comparison/) for the boundaries and positioning.

## Installation

```bash
python -m pip install mol-tdn
```

Python 3.9 or newer is required. Plotly and Matplotlib are included.

## Quick start

```python
from mol_tdn import Molecule, compute_eos

methane = Molecule("methane")
state = compute_eos(methane, t=298, p=100, eos="pr")

print(state.fugacity, state.fugacity_unit)
print(state.density, state.density_unit)
print(state.explain())

# Existing dictionary-style access remains valid.
assert state["density"] == state.density
```

## Scan conditions

```python
from mol_tdn import scan_eos

table = scan_eos(
    methane,
    temperatures=[273.15, 298.15, 323.15],
    pressures=[1, 10, 25, 50, 100],
    eos="pr",
)
table.to_csv("methane-pr.csv", index=False)
```

## Plot with Plotly or Matplotlib

```python
from mol_tdn import plot_pv, plot_scan, set_default_backend

plot_pv(methane, t=298)  # Plotly is the default.

set_default_backend("matplotlib")
plot_scan(table, x="pressure", y="fugacity", color="temperature")

# A per-call override always wins.
figure = plot_pv(methane, t=298, backend="plotly", show=False)
```

## Documentation and development

The full guide covers [explainable results](https://danieleongari.github.io/mol-tdn/results/), [scans](https://danieleongari.github.io/mol-tdn/scans/), [plotting](https://danieleongari.github.io/mol-tdn/plotting/), equations, units, limitations, and API details.

```bash
python -m pip install -e ".[dev]"
pytest --cov=mol_tdn --cov-report=term-missing
mkdocs build --strict
python -m build
```

Bug reports and focused contributions are welcome in [GitHub Issues](https://github.com/danieleongari/mol-tdn/issues).
