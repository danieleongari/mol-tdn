# Plotting

Plotly is the default backend. Every plotting function returns its native figure and accepts a per-call backend override.

=== "Plotly"

    ```python
    from mol_tdn import Molecule, plot_pv

    methane = Molecule("methane")
    figure = plot_pv(methane, t=298, backend="plotly")
    ```

=== "Matplotlib"

    ```python
    figure = plot_pv(methane, t=298, backend="matplotlib")
    figure.savefig("methane-pv.png", dpi=300, bbox_inches="tight")
    ```

Set the process-wide default when a notebook or project consistently uses one renderer:

```python
from mol_tdn import set_default_backend

set_default_backend("matplotlib")
```

## Scan plots

```python
from mol_tdn import plot_scan, scan_eos

table = scan_eos(methane, [280, 300, 320], [1, 10, 25, 50])
plot_scan(table, x="pressure", y="fugacity", color="temperature")
```

## Root diagnostics

```python
from mol_tdn import compute_eos, plot_roots

state = compute_eos(methane, t=150, p=15)
plot_roots(state)
```

Pass `show=False` in tests, batch jobs, or whenever the caller should decide when to display or save the returned figure.
