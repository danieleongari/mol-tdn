# API reference

## State calculations

### `compute_eos(mol, t, p=None, v=None, eos="pr", plot_fz=False)`

Compute a pure-fluid state. Supply exactly one of pressure `p` in bar or molar volume `v` in L/mol. Returns `EosResult`.

### `scan_eos(mol, temperatures, pressures, eos="pr")`

Evaluate a Cartesian grid and return a pandas DataFrame.

## Results

### `EosResult`

Read-only mapping with selected state properties, `roots`, `selected_root`, `selected_root_index`, `selection_reason`, `parameters`, `to_dict()`, and `explain()`.

### `RootResult`

Immutable properties for one physical compressibility root.

## Plotting

- `plot_pv(mol, t, eos=(...), ..., backend=None, show=True)`
- `plot_scan(frame, x="pressure", y="fugacity", color="temperature", backend=None, show=True)`
- `plot_roots(result, backend=None, show=True)`
- `set_default_backend(backend)`
- `get_default_backend()`
