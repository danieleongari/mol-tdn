"""Tests shared plotting behavior across native backends."""

import matplotlib.figure
import plotly.graph_objects as go
import pytest

from mol_tdn import (
    Molecule,
    compute_eos,
    get_default_backend,
    plot_pv,
    plot_roots,
    plot_scan,
    scan_eos,
    set_default_backend,
)


@pytest.fixture(autouse=True)
def restore_backend():
    original = get_default_backend()
    yield
    set_default_backend(original)


def test_backend_configuration_and_validation():
    assert get_default_backend() == "plotly"
    set_default_backend("matplotlib")
    assert get_default_backend() == "matplotlib"
    with pytest.raises(ValueError, match="backend"):
        set_default_backend("ascii")


@pytest.mark.parametrize(
    "backend, expected_type",
    [("plotly", go.Figure), ("matplotlib", matplotlib.figure.Figure)],
)
def test_pv_plot_backends(backend, expected_type):
    figure = plot_pv(Molecule("methane"), 298, eos=["pr", "rks"],
                     points=20, backend=backend, show=False)
    assert isinstance(figure, expected_type)
    count = len(figure.data) if backend == "plotly" else len(figure.axes[0].lines)
    assert count >= 2


@pytest.mark.parametrize("backend", ["plotly", "matplotlib"])
def test_scan_and_root_plots(backend):
    methane = Molecule("methane")
    frame = scan_eos(methane, [280, 300], [1, 10])
    scan_figure = plot_scan(frame, backend=backend, show=False)
    root_figure = plot_roots(compute_eos(methane, 150, p=15),
                             backend=backend, show=False)
    if backend == "plotly":
        assert len(scan_figure.data) == 2
        assert len(root_figure.data) == 3
    else:
        assert scan_figure.axes[0].get_xlabel() == "pressure"
        assert root_figure.axes[0].get_xlabel().startswith("Compressibility")


def test_plot_call_overrides_configured_default():
    set_default_backend("matplotlib")
    figure = plot_pv(Molecule("methane"), 298, eos="pr",
                     backend="plotly", points=10, show=False)
    assert isinstance(figure, go.Figure)


def test_scan_plot_rejects_missing_or_nonnumeric_columns():
    frame = scan_eos(Molecule("methane"), 298, [1, 10])
    with pytest.raises(ValueError, match="Missing"):
        plot_scan(frame, y="missing", show=False)
    with pytest.raises(TypeError, match="numeric"):
        plot_scan(frame, color="phase", show=False)
