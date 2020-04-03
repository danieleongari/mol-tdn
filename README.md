# mol-TDN: Thermodynamic properties of molecular fluids

## Examples
* Compute density of methane at 100 bar using the Peng-Robinson equation of state:

```
from mol_tdn import Molecule, compute_eos, plot_pv
m = Molecule('methane')
m.info()

    Molecule: methane
        Chemical formula: CH4
        Molecular Mass: 16.0 g/mol
        Critical Temperature: 190.56 K
        Critical Pressure: 45.99 bar
        Accentric factor: 0.012

compute_eos(m, t=298, p=100, eos='pr')

    {'temperature': 298,
    'temperature_unit': 'K',
    'temperature_reduced': 1.5638119227539882,
    'pressure': 100,
    'pressure_unit': 'bar',
    'pressure_reduced': 2.1743857360295715,
    'molar_density': 4864384.638349054,
    'molar_density_unit': 'mol/L',
    'density': 78019.8652144805,
    'density_unitg/cm^3fugacity_coefficient': 0.8192332007144563,
    'compressibility_factor': 0.8297472227294393,
    'fugacity': 81.92332007144563,
    'fugaciy_unit': 'bar',
    'molar_volume': 2.055758486112222e-07,
    'molar_volume_unit': 'L/mol',
    'enthalpy_reduced': -1.782712460028914,
    'enthalpy_reduced_unit': 'kJ/mol',
    'entropy_reduced': -0.004324557238707323,
    'entropy_reduced_unit': 'kJ/mol/K',
    'energy_gibbs_reduced': -0.4939944028941317,
    'energy_gibbs_reduced_unit': 'kJ/mol'}
```
