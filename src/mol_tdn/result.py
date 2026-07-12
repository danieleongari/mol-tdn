"""Structured, mapping-compatible results from cubic EOS calculations."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True)
class RootResult:
    """Properties associated with one physical compressibility root."""

    compressibility_factor: float
    fugacity_coefficient: float
    molar_volume: float
    molar_density: float
    density: float
    enthalpy_residual: float
    entropy_residual: float
    gibbs_energy_residual: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class EosResult(Mapping[str, Any]):
    """An explainable EOS state that remains compatible with dictionaries."""

    molecule: str
    eos: str
    phase: str
    temperature: float
    pressure: float
    temperature_reduced: float
    pressure_reduced: float
    roots: tuple[RootResult, ...]
    selected_root_index: int
    selection_reason: str
    parameters: Mapping[str, Any]

    def __post_init__(self):
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    @property
    def selected_root(self):
        return self.roots[self.selected_root_index]

    def _mapping(self):
        root = self.selected_root
        return {
            "phase": self.phase,
            "temperature": self.temperature,
            "temperature_unit": "K",
            "temperature_reduced": self.temperature_reduced,
            "pressure": self.pressure,
            "pressure_unit": "bar",
            "pressure_reduced": self.pressure_reduced,
            "molar_density": root.molar_density,
            "molar_density_unit": "mol/L",
            "density": root.density,
            "density_unit": "g/cm^3",
            "fugacity_coefficient": root.fugacity_coefficient,
            "compressibility_factor": root.compressibility_factor,
            "fugacity": root.fugacity_coefficient * self.pressure,
            "fugacity_unit": "bar",
            "fugaciy_unit": "bar",
            "molar_volume": root.molar_volume,
            "molar_volume_unit": "L/mol",
            "enthalpy_reduced": root.enthalpy_residual,
            "enthalpy_reduced_unit": "kJ/mol",
            "entropy_reduced": root.entropy_residual,
            "entropy_reduced_unit": "kJ/mol/K",
            "energy_gibbs_reduced": root.gibbs_energy_residual,
            "energy_gibbs_reduced_unit": "kJ/mol",
        }

    def __getitem__(self, key):
        return self._mapping()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._mapping())

    def __len__(self):
        return len(self._mapping())

    def __getattr__(self, name):
        mapping = self._mapping()
        if name in mapping:
            return mapping[name]
        raise AttributeError(name)

    def to_dict(self):
        """Return selected state properties as a plain dictionary."""
        return dict(self._mapping())

    def explain(self):
        """Return a deterministic, human-readable root-selection report."""
        lines = [
            f"{self.eos.upper()} state for {self.molecule}",
            f"Condition: T={self.temperature:g} K, P={self.pressure:g} bar",
            f"Physical roots: {len(self.roots)}",
        ]
        for index, root in enumerate(self.roots):
            marker = "selected" if index == self.selected_root_index else "candidate"
            lines.append(
                f"  [{index}] Z={root.compressibility_factor:.8g}, "
                f"phi={root.fugacity_coefficient:.8g} ({marker})"
            )
        lines.extend((
            f"Selection: {self.selection_reason}",
            f"Phase label: {self.phase}",
        ))
        return "\n".join(lines)
