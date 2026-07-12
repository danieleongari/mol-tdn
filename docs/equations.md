# Equations and units

## Generalized cubic form

The solver represents the four supported models as

\[
P = \frac{RT}{v-b} - \frac{a\alpha(T)}{(v+\delta_1 b)(v+\delta_2 b)}.
\]

It transforms this expression into a cubic polynomial in the compressibility factor \(Z\), retains finite real roots satisfying \(Z>B\), evaluates fugacity for each root, and selects the minimum-fugacity state.

| Identifier | Model | Temperature attraction | \(\delta_1, \delta_2\) |
| --- | --- | --- | --- |
| `vdw` | van der Waals | constant | 0, 0 |
| `rk` | Redlich–Kwong | \(T_r^{-1/2}\) | 1, 0 |
| `rks` | Soave–Redlich–Kwong | Soave alpha | 1, 0 |
| `pr` | Peng–Robinson | Peng–Robinson alpha | \(1+\sqrt 2, 1-\sqrt 2\) |

The implementation follows the original model definitions: [Redlich and Kwong (1949)](https://doi.org/10.1021/ie50488a008), [Soave (1972)](https://doi.org/10.1016/0009-2509%2872%2980096-4), and [Peng and Robinson (1976)](https://doi.org/10.1021/i160057a011). Regression tests fix representative methane values so changes to constants, alpha functions, root filtering, or residual-property expressions are visible in review. At 298 K and 100 bar, the PR and SRK compressibility factors and fugacity coefficients were independently cross-checked against CoolProp 8.0.0; relative differences were below 0.025%, consistent with the slightly different constants and fluid data used by the packages.

## Public units

| Quantity | Unit |
| --- | --- |
| Temperature | K |
| Pressure and fugacity | bar |
| Molar volume | L/mol |
| Molar density | mol/L |
| Mass density | g/cm³ |
| Residual enthalpy and Gibbs energy | kJ/mol |
| Residual entropy | kJ/(mol·K) |

The numerical core converts public molar-volume inputs to m³/mol before evaluating the pressure equation.
