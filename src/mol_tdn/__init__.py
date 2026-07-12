"""mol-tdn package."""

from .get_data import MOLECULE_DF, PERIODIC_TABLE_DF
from .molecule import Molecule
from .eos import SUPPORTED_EOS, compute_eos, get_eos, scan_eos
from .plot import (
    get_default_backend,
    plot_pv,
    plot_roots,
    plot_scan,
    set_default_backend,
)
from .result import EosResult, RootResult

__version__ = "0.0.1"

__all__ = [
    "EosResult",
    "Molecule",
    "RootResult",
    "SUPPORTED_EOS",
    "compute_eos",
    "get_default_backend",
    "get_eos",
    "plot_pv",
    "plot_roots",
    "plot_scan",
    "scan_eos",
    "set_default_backend",
]
