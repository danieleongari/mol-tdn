"""Tests for generated documentation plot artifacts."""

from pathlib import Path

from PIL import Image

from scripts.generate_plot_gallery import generate_gallery


def test_generate_gallery(tmp_path):
    output = generate_gallery(tmp_path / "gallery")
    expected_pngs = {
        "pv-comparison.png",
        "fugacity-scan.png",
        "root-selection.png",
    }
    pngs = {path.name for path in (output / "matplotlib").glob("*.png")}
    assert pngs == expected_pngs
    for name in expected_pngs:
        with Image.open(output / "matplotlib" / name) as image:
            assert image.width >= 1000
            assert image.height >= 600

    html_path = output / "plotly" / "gallery.html"
    html = html_path.read_text(encoding="utf-8")
    assert html.startswith("<!doctype html>")
    assert html.count("plotly-graph-div") == 3
    assert "plotly.js" in html
    assert html_path.stat().st_size > 1_000_000
