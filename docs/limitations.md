# Limitations

`mol-tdn` is pre-alpha research software. Its outputs must be independently validated for consequential use.

- Only pure fluids are supported; there are no mixing rules or binary interaction parameters.
- Phase labels are descriptive results of cubic-root selection, not a general flash calculation.
- Cubic EOS can be inaccurate for associating, polar, quantum, and near-critical fluids.
- The bundled molecule table is compact and is not a curated reference database.
- Transport properties, heat capacities, reactions, solids, and adsorption models are outside the current scope.
- Numerical regression tests protect implementation behavior but do not constitute broad experimental validation.

For high-accuracy property work, consider a reference-quality implementation such as CoolProp or REFPROP and consult the primary literature for the selected model.
