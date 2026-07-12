"""Backend-neutral visualizations for EOS states and scans."""

from __future__ import annotations

import numpy as np
from pandas.api.types import is_numeric_dtype

from .eos import SUPPORTED_EOS, pressure_at_volume

_DEFAULT_BACKEND = "plotly"


def set_default_backend(backend):
    """Set the process-wide plotting backend."""
    global _DEFAULT_BACKEND
    _DEFAULT_BACKEND = _validate_backend(backend)


def get_default_backend():
    """Return the process-wide plotting backend name."""
    return _DEFAULT_BACKEND


def _validate_backend(backend):
    backend = (backend or _DEFAULT_BACKEND).lower()
    if backend not in {"plotly", "matplotlib"}:
        raise ValueError("backend must be 'plotly' or 'matplotlib'")
    return backend


def _finish(figure, backend, show):
    if show:
        if backend == "plotly":
            figure.show()
        else:
            import matplotlib.pyplot as plt
            plt.show()
    return figure


def plot_pv(mol, t, eos=SUPPORTED_EOS, plim=(-100, 100),
            vlim=(0.1, 10.0), points=500, backend=None, show=True):
    """Plot pressure against molar volume for one or more EOS models."""
    backend = _validate_backend(backend)
    models = [eos] if isinstance(eos, str) else list(eos)
    invalid = sorted(set(models) - set(SUPPORTED_EOS))
    if invalid:
        raise ValueError(f"Unsupported EOS models: {', '.join(invalid)}")
    volumes = np.geomspace(vlim[0], vlim[1], points)
    series = {}
    for model in models:
        pressures = []
        for volume in volumes:
            try:
                pressures.append(pressure_at_volume(mol, t, volume, model))
            except ValueError:
                pressures.append(np.nan)
        series[model] = pressures

    if backend == "plotly":
        import plotly.graph_objects as go
        figure = go.Figure()
        for model, pressures in series.items():
            figure.add_scatter(x=volumes, y=pressures, mode="lines",
                               name=model.upper())
        figure.update_layout(
            title=f"{mol.name}: pressure-volume isotherm at {t:g} K",
            xaxis_title="Molar volume (L/mol)",
            yaxis_title="Pressure (bar)",
        )
        figure.update_xaxes(type="log")
        figure.update_yaxes(range=list(plim))
    else:
        import matplotlib.pyplot as plt
        figure, axes = plt.subplots()
        for model, pressures in series.items():
            axes.semilogx(volumes, pressures, label=model.upper())
        axes.set(title=f"{mol.name}: pressure-volume isotherm at {t:g} K",
                 xlabel="Molar volume (L/mol)", ylabel="Pressure (bar)",
                 ylim=plim)
        axes.axhline(0, color="black", linewidth=0.8)
        axes.grid(True)
        axes.legend()
    return _finish(figure, backend, show)


def plot_scan(frame, x="pressure", y="fugacity", color="temperature",
              backend=None, show=True):
    """Plot two numeric columns from :func:`mol_tdn.scan_eos` output."""
    backend = _validate_backend(backend)
    missing = [column for column in (x, y, color) if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing scan columns: {', '.join(missing)}")
    for column in (x, y, color):
        if not is_numeric_dtype(frame[column]):
            raise TypeError(f"Scan column {column!r} must be numeric")

    if backend == "plotly":
        import plotly.express as px
        figure = px.line(frame, x=x, y=y, color=color, markers=True,
                         title=f"EOS scan: {y} against {x}")
    else:
        import matplotlib.pyplot as plt
        figure, axes = plt.subplots()
        for value, group in frame.groupby(color, sort=False):
            axes.plot(group[x], group[y], marker="o", label=f"{color}={value}")
        axes.set(title=f"EOS scan: {y} against {x}", xlabel=x, ylabel=y)
        axes.grid(True)
        axes.legend()
    return _finish(figure, backend, show)


def plot_roots(result, backend=None, show=True):
    """Plot the EOS cubic polynomial and its physical roots."""
    backend = _validate_backend(backend)
    coefficients = result.parameters["cubic_coefficients"]
    roots = [root.compressibility_factor for root in result.roots]
    lower = min(-0.1, min(roots) - 0.2)
    upper = max(1.2, max(roots) + 0.2)
    z_values = np.linspace(lower, upper, 500)
    values = np.polyval(coefficients, z_values)
    selected = roots[result.selected_root_index]

    if backend == "plotly":
        import plotly.graph_objects as go
        figure = go.Figure()
        figure.add_scatter(x=z_values, y=values, mode="lines", name="f(Z)")
        figure.add_scatter(x=roots, y=[0] * len(roots), mode="markers",
                           name="physical roots")
        figure.add_scatter(x=[selected], y=[0], mode="markers",
                           marker={"size": 13, "symbol": "diamond"},
                           name="selected root")
        figure.update_layout(title="Compressibility-root selection",
                             xaxis_title="Compressibility factor, Z",
                             yaxis_title="Cubic polynomial, f(Z)")
    else:
        import matplotlib.pyplot as plt
        figure, axes = plt.subplots()
        axes.plot(z_values, values, label="f(Z)")
        axes.scatter(roots, [0] * len(roots), label="physical roots")
        axes.scatter([selected], [0], marker="D", s=75,
                     label="selected root")
        axes.axhline(0, color="black", linewidth=0.8)
        axes.set(title="Compressibility-root selection",
                 xlabel="Compressibility factor, Z",
                 ylabel="Cubic polynomial, f(Z)")
        axes.grid(True)
        axes.legend()
    return _finish(figure, backend, show)
