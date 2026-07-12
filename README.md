# mol-tdn

[![CI](https://github.com/danieleongari/mol-tdn/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleongari/mol-tdn/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/mol-tdn.svg)](https://pypi.org/project/mol-tdn/)
[![Python](https://img.shields.io/pypi/pyversions/mol-tdn.svg)](https://pypi.org/project/mol-tdn/)
[![codecov](https://codecov.io/gh/danieleongari/mol-tdn/branch/master/graph/badge.svg)](https://codecov.io/gh/danieleongari/mol-tdn)

`mol-tdn` is a small Python library for estimating thermodynamic properties of pure molecular fluids with cubic equations of state. It includes a built-in molecule database, supports manually supplied critical properties, and can produce pressure-volume plots.

> [!WARNING]
> This project is pre-alpha research software. Validate results independently before using them in scientific, engineering, or safety-critical work.

## Features

- van der Waals (`vdw`)
- Redlich-Kwong (`rk`)
- Soave-Redlich-Kwong (`rks`)
- Peng-Robinson (`pr`, the default)
- properties including density, molar volume, compressibility factor, fugacity, and residual thermodynamic quantities
- bundled molecular and periodic-table data
- custom molecules defined from a formula and critical properties

## Installation

Install the released package from PyPI:

```bash
python -m pip install mol-tdn
```

The package requires Python 3.9 or newer. To work from source, see [Development](#development).

## Quick start

Compute methane properties at 298 K and 100 bar with the Peng-Robinson equation of state:

```python
from mol_tdn import Molecule, compute_eos

methane = Molecule("methane")
result = compute_eos(methane, t=298, p=100, eos="pr")

print(f"Phase: {result['phase']}")
print(f"Density: {result['density']:.4f} {result['density_unit']}")
print(
    "Compressibility factor: "
    f"{result['compressibility_factor']:.4f}"
)
```

`Molecule.info()` prints the input properties loaded from the bundled database:

```python
methane.info()
```

```text
Molecule: methane
    Chemical formula: CH4
    Molecular Mass: 16.0 g/mol
    Critical Temperature: 190.56 K
    Critical Pressure: 45.99 bar
    Accentric factor: 0.012
```

## Using the API

### Choose an equation of state

Pass one of the supported identifiers to `compute_eos`:

```python
result = compute_eos(methane, t=298, p=100, eos="vdw")
result = compute_eos(methane, t=298, p=100, eos="rk")
result = compute_eos(methane, t=298, p=100, eos="rks")
result = compute_eos(methane, t=298, p=100, eos="pr")
```

Supply exactly one of pressure (`p`, in bar) or molar volume (`v`, in L/mol). Temperature `t` is expressed in kelvin.

### Define a custom molecule

Provide its molecular formula, critical temperature in kelvin, critical pressure in bar, and acentric factor:

```python
custom_methane = Molecule(
    "custom-methane",
    formula="CH4",
    tc=190.56,
    pc=45.99,
    af=0.012,
)

result = compute_eos(custom_methane, t=298, p=100)
```

### Plot pressure against molar volume

```python
from mol_tdn import Molecule, plot_pv

methane = Molecule("methane")
plot_pv(methane, t=150, plim=(-20, 100), vlim=(0.05, 2.0))
```

The plot compares all four supported equations of state. `plot_pv` displays a Matplotlib figure and does not currently return the axes.

## Result fields and units

`compute_eos` returns a dictionary. Important fields include:

| Field | Meaning | Unit |
| --- | --- | --- |
| `phase` | Estimated phase label | — |
| `pressure` | Pressure | bar |
| `temperature` | Temperature | K |
| `molar_volume` | Molar volume | L/mol |
| `molar_density` | Molar density | mol/L |
| `density` | Mass density | g/cm³ |
| `compressibility_factor` | Compressibility factor, Z | — |
| `fugacity_coefficient` | Fugacity coefficient | — |
| `fugacity` | Fugacity | bar |
| `enthalpy_reduced` | Residual enthalpy | kJ/mol |
| `entropy_reduced` | Residual entropy | kJ/(mol·K) |
| `energy_gibbs_reduced` | Residual Gibbs energy | kJ/mol |

## Development

Clone the repository and install it in editable mode with development tools:

```bash
git clone https://github.com/danieleongari/mol-tdn.git
cd mol-tdn
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the test suite and build distributable artifacts:

```bash
pytest --cov=mol_tdn --cov-report=term-missing
python -m build
```

## Contributing

Bug reports, focused pull requests, and suggestions are welcome in [GitHub Issues](https://github.com/danieleongari/mol-tdn/issues). Please include a minimal reproducible example and the Python version you used.

## Project status

The public API and numerical behavior may change while the library remains pre-alpha. Current limitations include pure-fluid calculations only, a compact bundled molecule database, and limited numerical validation across phase boundaries.
