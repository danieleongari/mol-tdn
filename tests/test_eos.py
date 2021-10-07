from mol_tdn import Molecule, compute_eos


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
