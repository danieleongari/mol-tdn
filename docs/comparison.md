# Open-source ecosystem comparison

`mol-tdn` is intentionally narrower than the established thermodynamics projects below. This page helps users choose an appropriate tool; it is not a claim that one package is universally better.

## Methodology

The comparison uses public project documentation and GitHub repository metadata reviewed on **12 July 2026**. GitHub stars are a dated indicator of visibility, not scientific quality, accuracy, maintenance, or fitness for a particular calculation. Feature descriptions are intentionally high-level because project capabilities evolve.

| Project | Primary language | GitHub stars¹ | Main scope | Mixtures / flash | Built-in property data | Visualization focus |
| --- | --- | ---: | --- | --- | --- | --- |
| **mol-tdn** | Python | 2 | Explainable pure-fluid cubic EOS | No | Compact CSV tables | Plotly + Matplotlib root, scan, and P–V plots |
| [CoolProp](https://github.com/CoolProp/CoolProp) | C++ with Python API | 1,033 | High-accuracy thermophysical properties and multiple backends | Yes | Large fluid library | Examples; calculation-first API |
| [`thermo`](https://github.com/CalebBell/thermo) | Python | 766 | Chemical properties, phases, EOS, and flash calculations | Yes | Extensive ChEDL data | Calculation-first API |
| [Clapeyron.jl](https://github.com/ClapeyronThermo/Clapeyron.jl) | Julia | 286 | Extensible EOS and phase-equilibrium framework | Yes | Model/component data | Research/model-development workflows |
| [Phasepy](https://github.com/gustavochm/phasepy) | Python | 108 | Cubic EOS, activity models, and phase equilibrium | Yes | Component objects | Phase-diagram workflows |
| [Thermopack](https://github.com/thermotools/thermopack) | Fortran with wrappers | 102 | Fluid models, PVT properties, and equilibria | Yes | Model databases | Calculation-first API |
| [PYroMat](https://github.com/chmarti1/PYroMat) | Python | 83 | Accessible thermodynamic-property calculations | Limited by collection | Packaged species collections | Educational calculation workflows |
| [teqp](https://github.com/usnistgov/teqp) | C++ with Python API | 82 | Fast, differentiable EOS model evaluation | Yes | Model-oriented | Numerical/model-development focus |
| [Thermosteam](https://github.com/BioSTEAMDevelopmentGroup/thermosteam) | Python | 76 | Process-oriented thermodynamics and chemical streams | Yes | Chemical/property integration | Process-simulation workflows |
| [PREOS](https://github.com/CorySimon/PREOS) | Python | 42 | Focused Peng–Robinson calculation | Limited | Minimal | Small educational implementation |
| [pythermophy](https://github.com/j-jith/pythermophy) | Python | 21 | Pure-fluid density, heat capacity, and sound speed from EOS | No | Small fluid set | Calculation-first API |

¹ Star counts are a snapshot retrieved from GitHub on 12 July 2026 and will become stale.

## Where the projects overlap

### CoolProp

CoolProp is the natural choice for broad, high-accuracy thermophysical properties, many fluids, multiple language wrappers, and established reference equations. It includes PR and SRK cubic backends alongside more accurate formulations. `mol-tdn` complements it when the calculation trace, individual roots, compact Python implementation, or side-by-side cubic-model visualization matters more than database breadth.

### `thermo`

`thermo` is a comprehensive chemical-engineering library with property correlations, phase objects, mixture models, and flash solvers. Choose it for application breadth and process calculations. Choose `mol-tdn` for a smaller pure-fluid exercise or research preprocessing step where every EOS root and selection decision should remain visible.

### Phasepy

Phasepy covers pure components and mixtures, volume translation, activity-coefficient models, mixing rules, and phase-equilibrium calculations. It is much closer to a phase-equilibrium research framework. `mol-tdn` deliberately avoids that model breadth and concentrates on an approachable state/scan/plot workflow.

### Thermopack and teqp

Thermopack and teqp emphasize capable, high-performance thermodynamic model engines. They are appropriate when advanced models, mixture behavior, derivatives, or computational performance dominate. `mol-tdn` favors inspectability and ordinary Python objects over a compiled high-performance core.

### Thermosteam

Thermosteam serves material streams, reactions, phase equilibrium, and BioSTEAM process models. Its natural unit of work is a process stream or simulation. `mol-tdn` works at the smaller boundary between a molecule, an experimental condition, and a transparent cubic-EOS estimate.

### PREOS and pythermophy

These are the closest small Python projects. PREOS is a concise Peng–Robinson implementation, while pythermophy predicts several pure-fluid properties with multiple EOS models. `mol-tdn` differentiates itself through a mapping-compatible explainable result, explicit root-selection trace, tidy grid scans, and interchangeable interactive/static plotting.

### PYroMat and Clapeyron.jl

PYroMat prioritizes accessible thermodynamic-property use in Python, including educational contexts. Clapeyron.jl provides a broad, modern Julia framework for developing and using cubic, SAFT, activity, multiparameter, and COSMO-based models. `mol-tdn` occupies a smaller Python niche: auditable cubic EOS for pure fluids, especially for fugacity/density preprocessing and model comparison.

## Choosing a package

- Use **CoolProp** for established, high-accuracy fluid properties.
- Use **`thermo`**, **Phasepy**, **Thermopack**, or **Thermosteam** for mixtures, phase equilibrium, or process workflows.
- Use **teqp** or **Clapeyron.jl** for advanced EOS development and numerical work.
- Use **PYroMat** for broad educational property calculations.
- Use **PREOS** or **pythermophy** for other compact pure-fluid implementations.
- Use **mol-tdn** when an explainable cubic-EOS state, reproducible scan table, or root-aware visualization is the actual deliverable.

Corrections are welcome through [GitHub Issues](https://github.com/danieleongari/mol-tdn/issues), especially when another project adds or changes a capability represented here.
