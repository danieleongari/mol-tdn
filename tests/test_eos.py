from mol_tdn import Molecule, compute_eos
from mol_tdn.eos import EosParameters


def test_methane_params():
    """Check if the class EosParameters loads the parameters correctly."""
    ch4 = Molecule('methane')
    eosp = EosParameters(mol=ch4, t=298, eos='vdw')
    assert eosp.w == 0


def test_methane_eos():
    """Testing the EOS for Methane (in the database) at a certain T, P."""
    ch4 = Molecule('methane')
    eos = compute_eos(
        mol=ch4,
        t=298,  # K
        p=100,  # bar
        eos='pr',  # Peng-Robinson 
    )
    assert eos['temperature'] == 298


def test_methane_manual_eos():
    """Testing the EOS for Methane (in the database) at a certain T, P."""
    ch4 = Molecule('methane_manual', formula='CH4', tc=190, pc=46, af=0.01)
    eos = compute_eos(
        mol=ch4,
        t=298,  # K
        p=100,  # bar
        eos='pr',  # Peng-Robinson 
    )
    assert eos['temperature'] == 298
