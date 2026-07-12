# Scans and data export

`scan_eos` evaluates the Cartesian product of temperatures and pressures and returns a tidy pandas DataFrame.

```python
from mol_tdn import Molecule, scan_eos

methane = Molecule("methane")
table = scan_eos(
    methane,
    temperatures=[273.15, 298.15, 323.15],
    pressures=[1, 5, 10, 25, 50, 100],
    eos="pr",
)

table.to_csv("methane-pr.csv", index=False)
```

Each row contains the selected state, molecule and EOS identifiers, number of physical roots, selected root index, and selection reason. Row order follows temperature first and pressure second.

If a state cannot be evaluated, the scan stops and reports its exact temperature and pressure rather than silently dropping the row.
