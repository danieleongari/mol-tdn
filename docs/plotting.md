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

## Live Plotly gallery

The gallery below is generated from the public plotting API during every documentation workflow. It is interactive: zoom, pan, hover over values, and toggle traces from each legend.

<iframe
  src="../assets/generated/plotly/gallery.html"
  title="Interactive mol-tdn Plotly gallery"
  style="width: 100%; height: 1780px; border: 1px solid #cfd8dc; border-radius: 6px;"
  loading="lazy"
></iframe>

## Matplotlib gallery

These static figures are generated from the same inputs and are suitable as a starting point for reports and publications.

### Pressure–volume comparison

![Matplotlib pressure-volume comparison](assets/generated/matplotlib/pv-comparison.png)

### Fugacity scan

![Matplotlib fugacity scan](assets/generated/matplotlib/fugacity-scan.png)

### Compressibility-root selection

![Matplotlib root-selection plot](assets/generated/matplotlib/root-selection.png)

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

## Reproducing the gallery

Generate the same files locally:

```bash
MPLBACKEND=Agg python scripts/generate_plot_gallery.py
mkdocs serve
```

GitHub Actions uploads `docs/assets/generated` as a `plot-gallery-<commit>` artifact for 30 days. The artifact contains the three Matplotlib PNG files and a self-contained Plotly HTML gallery that can be opened offline.
