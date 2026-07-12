"""Regression and behavior tests for the generalized cubic solver."""

import numpy as np
import pytest

from mol_tdn import EosResult, Molecule, compute_eos, scan_eos
from mol_tdn.eos import pressure_at_volume


# Fixed methane regression values at 298 K and 100 bar. Equations, citations,
# and the independent CoolProp 8.0.0 PR/SRK cross-check are documented in
# docs/equations.md; one state makes changes in alpha/residual formulas visible.
REFERENCE = {
    "vdw": (0.8101205697, 0.8180425362, 0.0799100392, -1.6176104469),
    "rk": (0.8521450810, 0.8444614245, 0.0759691840, -1.6061609021),
    "rks": (0.8666260842, 0.8564289625, 0.0746997669, -1.6648530637),
    "pr": (0.8297472227, 0.8192332007, 0.0780198652, -1.7827124600),
}


@pytest.mark.parametrize("eos", REFERENCE)
def test_all_models_match_reference_state(eos):
    result = compute_eos(Molecule("methane"), t=298, p=100, eos=eos)
    expected = REFERENCE[eos]
    actual = (
        result.compressibility_factor,
        result.fugacity_coefficient,
        result.density,
        result.enthalpy_reduced,
    )
    assert actual == pytest.approx(expected, rel=1e-8)
    assert result.energy_gibbs_reduced == pytest.approx(
        result.enthalpy_reduced - 298 * result.entropy_reduced
    )


def test_result_is_mapping_with_explanation_and_aliases():
    result = compute_eos(Molecule("methane"), t=298, p=100)
    assert isinstance(result, EosResult)
    assert result["density"] == result.density
    assert result.to_dict()["fugacity_unit"] == "bar"
    assert result["fugaciy_unit"] == result["fugacity_unit"]
    assert result.selected_root is result.roots[result.selected_root_index]
    assert result.explain() == result.explain()
    assert "minimum" in result.selection_reason or "only" in result.selection_reason


def test_multiple_roots_select_minimum_fugacity():
    result = compute_eos(Molecule("methane"), t=150, p=15, eos="pr")
    assert len(result.roots) == 3
    expected = min(root.fugacity_coefficient for root in result.roots)
    assert result.selected_root.fugacity_coefficient == expected
    assert result.phase == "liquid"


def test_volume_input_round_trip_and_custom_molecule():
    methane = Molecule("custom", formula="CH4", tc=190.56, pc=45.99, af=0.012)
    state = compute_eos(methane, t=298, p=100, eos="pr")
    pressure = pressure_at_volume(methane, 298, state.molar_volume, eos="pr")
    recovered = compute_eos(methane, t=298, v=state.molar_volume, eos="pr")
    assert pressure == pytest.approx(100)
    assert recovered.pressure == pytest.approx(100)
    assert recovered.molar_volume == pytest.approx(state.molar_volume)


def test_ideal_gas_limit_and_near_critical_state():
    methane = Molecule("methane")
    dilute = compute_eos(methane, t=500, p=1e-4, eos="pr")
    assert dilute.compressibility_factor == pytest.approx(1, rel=1e-5)
    assert dilute.fugacity_coefficient == pytest.approx(1, rel=1e-5)
    critical = compute_eos(methane, t=methane.tc, p=methane.pc, eos="pr")
    assert np.isfinite(critical.compressibility_factor)
    assert critical.compressibility_factor > 0


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"t": 0, "p": 1}, "temperature"),
        ({"t": 298}, "exactly one"),
        ({"t": 298, "p": 1, "v": 1}, "exactly one"),
        ({"t": 298, "p": -1}, "pressure"),
        ({"t": 298, "p": 1, "eos": "magic"}, "Unknown EOS"),
    ],
)
def test_invalid_inputs(kwargs, message):
    with pytest.raises(ValueError, match=message):
        compute_eos(Molecule("methane"), **kwargs)


def test_scan_scalar_and_cartesian_grid():
    methane = Molecule("methane")
    scalar = scan_eos(methane, temperatures=298, pressures=1)
    assert len(scalar) == 1
    frame = scan_eos(methane, temperatures=[280, 300], pressures=[1, 10])
    assert list(frame[["temperature", "pressure"]].itertuples(index=False, name=None)) == [
        (280, 1), (280, 10), (300, 1), (300, 10)
    ]
    assert {"molecule", "eos", "root_count", "selection_reason"} <= set(frame)


def test_scan_reports_failing_condition():
    with pytest.raises(RuntimeError, match=r"T=-1 K, P=1 bar"):
        scan_eos(Molecule("methane"), temperatures=[298, -1], pressures=[1])
