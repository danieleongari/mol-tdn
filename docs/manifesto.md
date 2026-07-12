# Project manifesto

## Purpose

`mol-tdn` exists to make pure-fluid cubic equations of state transparent and convenient for molecular simulation, adsorption research, teaching, and reproducible model comparison.

It should be especially useful when a researcher has critical temperature, critical pressure, and an acentric factor and needs a traceable estimate of density, fugacity, compressibility, or residual properties.

## Principles

1. **Show the reasoning.** Preserve roots, EOS parameters, units, and the reason a state was selected.
2. **Prefer reproducible tables.** Treat pressure/temperature scans and data export as first-class workflows.
3. **Keep plotting portable.** Offer interactive exploration with Plotly and static, publication-oriented figures with Matplotlib.
4. **Stay small enough to audit.** A motivated researcher should be able to read the numerical core.
5. **State limitations plainly.** Convenience must not be confused with reference-quality property data.

## Deliberate boundaries

`mol-tdn` is not intended to become:

- a full process simulator;
- a comprehensive chemical-property database;
- a transport-property package;
- a general multiphase or reactive flash engine;
- a replacement for CoolProp, REFPROP, `thermo`, Phasepy, or Thermopack.

Mixtures and adsorption-specific exports may be explored later, but the present contract is pure fluids. This boundary lets the project improve explainability and research ergonomics without copying the breadth of mature thermodynamics systems.
