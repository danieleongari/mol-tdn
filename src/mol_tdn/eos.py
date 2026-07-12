"""Transparent cubic equations of state for pure fluids."""

from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt
from numbers import Real
from typing import Iterable

import numpy as np
import pandas as pd

from .get_data import R
from .result import EosResult, RootResult

SUPPORTED_EOS = ("vdw", "rk", "rks", "pr")


@dataclass
class EosParameters:
    """Temperature-dependent parameters for a generalized cubic EOS."""

    eos: str
    tr: float
    a: float
    b: float
    alpha: float
    dln_alpha_dln_t: float
    u: float
    w: float
    delta_1: float
    delta_2: float

    @property
    def a_alpha(self):
        return self.a * self.alpha

    @classmethod
    def create(cls, mol, temperature, eos):
        eos = eos.lower()
        if eos not in SUPPORTED_EOS:
            choices = ", ".join(SUPPORTED_EOS)
            raise ValueError(f"Unknown EOS {eos!r}; choose one of: {choices}")

        tr = temperature / mol.tc
        if eos == "vdw":
            return cls(eos, tr, 0.421875 * R**2 * mol.tc**2 / mol.pc,
                       0.125 * R * mol.tc / mol.pc, 1.0, 0.0, 0.0, 0.0,
                       0.0, 0.0)
        if eos == "rk":
            return cls(eos, tr, 0.42748 * R**2 * mol.tc**2 / mol.pc,
                       0.08664 * R * mol.tc / mol.pc, tr**-0.5, -0.5,
                       1.0, 0.0, 1.0, 0.0)
        if eos == "rks":
            m = 0.48 + 1.574 * mol.af - 0.176 * mol.af**2
            base = 1.0 + m * (1.0 - sqrt(tr))
            alpha = base**2
            derivative = -m * sqrt(tr) / base
            return cls(eos, tr, 0.42748 * R**2 * mol.tc**2 / mol.pc,
                       0.08664 * R * mol.tc / mol.pc, alpha, derivative,
                       1.0, 0.0, 1.0, 0.0)

        m = 0.37464 + 1.54226 * mol.af - 0.26992 * mol.af**2
        base = 1.0 + m * (1.0 - sqrt(tr))
        alpha = base**2
        derivative = -m * sqrt(tr) / base
        return cls(eos, tr, 0.45724 * R**2 * mol.tc**2 / mol.pc,
                   0.07780 * R * mol.tc / mol.pc, alpha, derivative,
                   2.0, -1.0, 1.0 + sqrt(2.0), 1.0 - sqrt(2.0))


def pressure_at_volume(mol, temperature, molar_volume, eos="pr"):
    """Return pressure in bar for a public molar-volume input in L/mol."""
    _validate_positive("temperature", temperature)
    _validate_positive("molar_volume", molar_volume)
    parameters = EosParameters.create(mol, temperature, eos)
    volume = molar_volume / 1000.0
    if volume <= parameters.b:
        raise ValueError(
            f"molar_volume must exceed the EOS covolume "
            f"({parameters.b * 1000:.6g} L/mol)"
        )
    denominator = (volume + parameters.delta_1 * parameters.b) * (
        volume + parameters.delta_2 * parameters.b)
    return (R * temperature / (volume - parameters.b)
            - parameters.a_alpha / denominator)


def _validate_positive(name, value):
    if not isinstance(value, Real) or not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive finite number")


def _attraction_integral(z_value, b_value, parameters):
    if parameters.delta_1 == parameters.delta_2:
        return b_value / z_value
    ratio = ((z_value + parameters.delta_1 * b_value)
             / (z_value + parameters.delta_2 * b_value))
    return log(ratio) / (parameters.delta_1 - parameters.delta_2)


def _root_properties(z_value, a_value, b_value, parameters, temperature,
                     pressure, mol):
    integral = _attraction_integral(z_value, b_value, parameters)
    attraction = a_value / b_value * integral if b_value > 1e-14 else 0.0
    ln_phi = z_value - 1.0 - log(z_value - b_value) - attraction
    h_adim = (z_value - 1.0
              + attraction * (parameters.dln_alpha_dln_t - 1.0))
    s_adim = (log(z_value - b_value)
              + attraction * parameters.dln_alpha_dln_t)
    g_adim = h_adim - s_adim
    molar_density = pressure / (R * 1000.0 * temperature * z_value)
    return RootResult(
        compressibility_factor=z_value,
        fugacity_coefficient=float(np.exp(ln_phi)),
        molar_volume=1.0 / molar_density,
        molar_density=molar_density,
        density=molar_density * mol.mm / 1000.0,
        enthalpy_residual=h_adim * R * 100.0 * temperature,
        entropy_residual=s_adim * R * 100.0,
        gibbs_energy_residual=g_adim * R * 100.0 * temperature,
    )


def _phase_label(mol, temperature, pressure, root_index, root_count):
    if temperature >= mol.tc and pressure >= mol.pc:
        return "supercritical"
    if root_count > 1:
        return "liquid" if root_index == 0 else "gas"
    return "gas" if temperature >= mol.tc else "single-phase"


def get_eos(mol, t, p=None, v=None, eos="pr", plot_fz=False):
    """Compute a pure-fluid state with a cubic equation of state.

    Temperature is in K, pressure in bar, and molar volume in L/mol.
    Exactly one of ``p`` and ``v`` must be supplied. ``plot_fz`` is retained
    for compatibility; it delegates to :func:`mol_tdn.plot_roots`.
    """
    _validate_positive("temperature", t)
    if (p is None) == (v is None):
        raise ValueError("Specify exactly one of pressure or molar volume")
    if p is not None:
        _validate_positive("pressure", p)
    else:
        p = pressure_at_volume(mol, t, v, eos=eos)
        _validate_positive("calculated pressure", p)

    parameters = EosParameters.create(mol, t, eos)
    a_value = parameters.a_alpha * p / (R**2 * t**2)
    b_value = parameters.b * p / (R * t)
    coefficients = (
        1.0,
        -1.0 - b_value + parameters.u * b_value,
        a_value + parameters.w * b_value**2 - parameters.u * b_value
        - parameters.u * b_value**2,
        -a_value * b_value - parameters.w * b_value**2
        - parameters.w * b_value**3,
    )
    raw_roots = np.roots(coefficients)
    physical_z = sorted({
        float(root.real)
        for root in raw_roots
        if abs(root.imag) <= 1e-8 and root.real > max(b_value, 0.0) + 1e-10
    })
    if not physical_z:
        raise RuntimeError(
            f"No physical roots for {mol.name} at T={t} K and P={p} bar"
        )

    roots = tuple(_root_properties(z_value, a_value, b_value, parameters,
                                   t, p, mol) for z_value in physical_z)
    if v is None:
        selected_index = min(
            range(len(roots)), key=lambda index: roots[index].fugacity_coefficient)
        reason = ("only physical root" if len(roots) == 1 else
                  "minimum fugacity coefficient among physical roots")
    else:
        selected_index = min(
            range(len(roots)), key=lambda index: abs(roots[index].molar_volume - v))
        reason = "physical root closest to the supplied molar volume"

    selected = roots[selected_index]
    result = EosResult(
        molecule=mol.name,
        eos=parameters.eos,
        phase=_phase_label(mol, t, p, selected_index, len(roots)),
        temperature=t,
        pressure=p,
        temperature_reduced=parameters.tr,
        pressure_reduced=p / mol.pc,
        roots=roots,
        selected_root_index=selected_index,
        selection_reason=reason,
        parameters={
            "a": parameters.a,
            "b": parameters.b,
            "alpha": parameters.alpha,
            "A": a_value,
            "B": b_value,
            "cubic_coefficients": coefficients,
        },
    )
    if plot_fz:
        from .plot import plot_roots
        plot_roots(result)
    return result


def compute_eos(mol, t, p=None, v=None, eos="pr", plot_fz=False):
    """Public compatibility wrapper for :func:`get_eos`."""
    return get_eos(mol, t=t, p=p, v=v, eos=eos, plot_fz=plot_fz)


def _as_values(values, name):
    if isinstance(values, Real):
        values = [values]
    elif isinstance(values, Iterable) and not isinstance(values, (str, bytes)):
        values = list(values)
    else:
        raise TypeError(f"{name} must be a number or iterable of numbers")
    if not values:
        raise ValueError(f"{name} cannot be empty")
    return values


def scan_eos(mol, temperatures, pressures, eos="pr"):
    """Evaluate a Cartesian temperature/pressure grid as a tidy DataFrame."""
    temperatures = _as_values(temperatures, "temperatures")
    pressures = _as_values(pressures, "pressures")
    rows = []
    for temperature in temperatures:
        for pressure in pressures:
            try:
                result = compute_eos(mol, t=temperature, p=pressure, eos=eos)
            except Exception as exc:
                raise RuntimeError(
                    f"EOS scan failed at T={temperature} K, P={pressure} bar"
                ) from exc
            row = result.to_dict()
            row.update({
                "molecule": mol.name,
                "eos": eos.lower(),
                "root_count": len(result.roots),
                "selected_root_index": result.selected_root_index,
                "selection_reason": result.selection_reason,
            })
            rows.append(row)
    return pd.DataFrame(rows)
