# Explainable results

`compute_eos` returns an `EosResult`. It behaves as a read-only mapping while exposing attributes and calculation details.

```python
state = compute_eos(Molecule("methane"), t=150, p=15, eos="pr")

state["fugacity"]
state.fugacity
state.to_dict()
```

## Inspect the roots

```python
for root in state.roots:
    print(root.compressibility_factor, root.fugacity_coefficient)

print(state.selected_root_index)
print(state.selection_reason)
print(state.explain())
```

For multiple physical roots, the solver chooses the candidate with the minimum fugacity coefficient. A calculation performed from a supplied molar volume chooses the root closest to that volume. All retained roots remain available for inspection.

## Inspect EOS parameters

```python
state.parameters["a"]
state.parameters["b"]
state.parameters["alpha"]
state.parameters["A"]
state.parameters["B"]
state.parameters["cubic_coefficients"]
```

The mapping is read-only so a reported state cannot be silently changed after calculation.
