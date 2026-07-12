# Explainable cubic equations of state

`mol-tdn` is a compact Python toolkit for pure-fluid cubic equations of state. It is designed for researchers who need to understand, inspect, visualize, and export the calculation—not merely obtain a number.

```python
from mol_tdn import Molecule, compute_eos

methane = Molecule("methane")
state = compute_eos(methane, t=298, p=100, eos="pr")

print(state.fugacity)
print(state.explain())
```

The same result supports legacy dictionary access:

```python
assert state["density"] == state.density
```

## What makes it different?

- Every physical compressibility root remains inspectable.
- Root and phase selection carries a human-readable explanation.
- Pressure/temperature grids become tidy pandas tables.
- Plotly and Matplotlib share the same plotting interface.
- The implementation stays small enough to study and audit.

!!! warning "Pre-alpha research software"
    Validate results independently before scientific, engineering, or safety-critical use. See [limitations](limitations.md).

[Read the manifesto](manifesto.md){ .md-button .md-button--primary }
[Start using the API](quickstart.md){ .md-button }
