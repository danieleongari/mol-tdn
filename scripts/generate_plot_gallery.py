"""Generate reproducible Matplotlib and Plotly documentation galleries."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.io as pio

from mol_tdn import Molecule, compute_eos, plot_pv, plot_roots, plot_scan, scan_eos


def _examples():
    methane = Molecule("methane")
    scan = scan_eos(
        methane,
        temperatures=[260, 280, 300, 320],
        pressures=[1, 5, 10, 25, 50, 75, 100],
        eos="pr",
    )
    multiroot = compute_eos(methane, t=150, p=15, eos="pr")
    return (
        (
            "Pressure–volume comparison",
            lambda backend: plot_pv(
                methane,
                t=150,
                eos=["vdw", "rk", "rks", "pr"],
                plim=(-25, 100),
                vlim=(0.04, 2.0),
                backend=backend,
                show=False,
            ),
        ),
        (
            "Fugacity scan",
            lambda backend: plot_scan(
                scan,
                x="pressure",
                y="fugacity",
                color="temperature",
                backend=backend,
                show=False,
            ),
        ),
        (
            "Compressibility-root selection",
            lambda backend: plot_roots(multiroot, backend=backend, show=False),
        ),
    )


def generate_gallery(output):
    """Generate static PNG files and one self-contained interactive HTML file."""
    output = Path(output)
    matplotlib_dir = output / "matplotlib"
    plotly_dir = output / "plotly"
    matplotlib_dir.mkdir(parents=True, exist_ok=True)
    plotly_dir.mkdir(parents=True, exist_ok=True)

    html_sections = []
    names = ("pv-comparison", "fugacity-scan", "root-selection")
    for index, ((title, factory), name) in enumerate(zip(_examples(), names)):
        static_figure = factory("matplotlib")
        static_figure.set_size_inches(8.5, 5.25)
        static_figure.tight_layout()
        static_figure.savefig(
            matplotlib_dir / f"{name}.png",
            dpi=160,
            bbox_inches="tight",
            metadata={"Software": "mol-tdn"},
        )
        plt.close(static_figure)

        interactive_figure = factory("plotly")
        interactive_figure.update_layout(template="plotly_white", height=520)
        div = pio.to_html(
            interactive_figure,
            full_html=False,
            include_plotlyjs=True if index == 0 else False,
            config={"responsive": True, "displaylogo": False},
        )
        html_sections.append(f"<section><h2>{title}</h2>{div}</section>")

    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>mol-tdn Plotly gallery</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 1rem; color: #263238; }
    section { margin: 0 0 2.5rem; }
    h2 { font-size: 1.15rem; margin: 0 0 .5rem; }
  </style>
</head>
<body>
""" + "\n".join(html_sections) + "\n</body>\n</html>\n"
    (plotly_dir / "gallery.html").write_text(html, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="docs/assets/generated",
        help="Directory for generated gallery files",
    )
    args = parser.parse_args()
    generate_gallery(args.output)


if __name__ == "__main__":
    main()
