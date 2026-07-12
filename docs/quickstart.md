# Quick start

## Installation

```bash
python -m pip install mol-tdn
```

Python 3.9 or newer is required. Plotly and Matplotlib are installed with the package.

## Calculate a state

```python
from mol_tdn import Molecule, compute_eos

methane = Molecule("methane")
state = compute_eos(methane, t=298, p=50, eos="pr")

print(f"Z = {state.compressibility_factor:.4f}")
print(f"f = {state.fugacity:.3f} {state.fugacity_unit}")
print(f"rho = {state.density:.4f} {state.density_unit}")
```

Supported EOS identifiers are `vdw`, `rk`, `rks`, and `pr`.

## Supply a molecule manually

```python
custom = Molecule(
    "custom-methane",
    formula="CH4",
    tc=190.56,
    pc=45.99,
    af=0.012,
)

state = compute_eos(custom, t=298, p=100)
```

Temperature is expressed in K, pressure in bar, and molar volume in L/mol.
