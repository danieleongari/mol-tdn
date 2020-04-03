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

    {'phase': 'supercritic',
    'temperature': 290,
    'temperature_unit': 'K',
    'temperature_reduced': 1.5218303946263645,
    'pressure': 100,
    'pressure_unit': 'bar',
    'pressure_reduced': 2.1743857360295715,
    'molar_density': 5.1136267891221125,
    'molar_density_unit': 'mol/L',
    'density': 0.08201746007072958,
    'density_unit': 'g/cm^3',
    'fugacity_coefficient': 0.8026596911737123,
    'compressibility_factor': 0.8110786197961839,
    'fugacity': 80.26596911737123,
    'fugaciy_unit': 'bar',
    'molar_volume': 0.1955559217045787,
    'molar_volume_unit': 'L/mol',
    'enthalpy_reduced': -1.8894059136250632,
    'enthalpy_reduced_unit': 'kJ/mol',
    'entropy_reduced': -0.004687572314523244,
    'entropy_reduced_unit': 'kJ/mol/K',
    'energy_gibbs_reduced': -0.530009942413322,
    'energy_gibbs_reduced_unit': 'kJ/mol'}
```
