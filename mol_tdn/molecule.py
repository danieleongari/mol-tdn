"""Tools for the Class Molecule."""
import re
from .get_data import MOLECULE_DF, PERIODIC_TABLE_DF


def search_in_csv(name):
    """Search for the molecular properties in the CSV database."""
    mol_row = MOLECULE_DF.loc[MOLECULE_DF['Name'] == name.lower()]  # pylint: disable=unsubscriptable-object
    if len(mol_row) == 0:
        raise AttributeError
    formula = mol_row.Formula.values[0]
    tc = mol_row["Tc(K)"].values[0]
    pc = mol_row["Pc(bar)"].values[0]
    af = mol_row.AcentricFactor.values[0]
    return formula, tc, pc, af


def get_mol_mass(formula):
    """Compute molecular mass from the chemical formula."""
    formula_split = re.sub(r"([A-Z])", r" \1", formula).split()  # 'CH4Xe23Na' > ['C', 'H4', 'Xe23', 'Na']
    mol_mass = 0
    for element in [re.split('(\d+)', x) for x in formula_split]:
        symbol = element[0]
        mass = PERIODIC_TABLE_DF[PERIODIC_TABLE_DF.Symbol == symbol]['AtomicMass'].values[0]
        coeff = int(element[1]) if len(element) > 1 else 1
        mol_mass += mass * coeff
    return mol_mass


class Molecule:
    """Molecular properties."""

    def __init__(self, name, formula=None, tc=None, pc=None, af=None):  #pylint: disable=too-many-arguments
        """Parameters describing the molecule."""
        self.name = name
        if all([formula, tc, pc, af]):
            self.data = 'manual'
        else:
            formula, tc, pc, af = search_in_csv(name)
            self.data = 'csv'

        self.formula = formula
        self.tc = tc
        self.tc_unit = 'K'
        self.pc = pc
        self.pc_unit = 'bar'
        self.af = af

        self.mm = get_mol_mass(self.formula)
        self.mm_unit = 'g/mol'

        self.vc, self.vc_eos = None, None

    def info(self):
        """Print molecule's info."""
        print(f"Molecule: {self.name}")
        print(f"\tChemical formula: {self.formula}")
        print(f"\tMolecular Mass: {self.mm:.1f} {self.mm_unit}")
        print(f"\tCritical Temperature: {self.tc:.2f} {self.tc_unit}")
        print(f"\tCritical Pressure: {self.pc:.2f} {self.pc_unit}")
        print(f"\tAccentric factor: {self.af:.3f}")
