"""Tools to plot nice diagrams."""
import numpy as np
# pylint: skip-file


def plot_eos(mol, xyz="vpt", eos="pr", xlim=None, ylim=None, zlim=None, pstep=0.1, tstep=10, xlog=None, ylog=None):
    """Plot EOS diagram:

    Parameters
    ----------
    mol: Molecule
        Molecule of the fluid.
    x: string in ["t","p","v"]
        Variable of the x axis.
    y: string in ["t","p","v"]
        Variable of the y axis.
    z: string
        Variable for the isovalue curves.
    xlim: list of floats, [min, max, ]

    """

    if (x, y, z) == ("v", "p", "t"):
        if not xlim:
            xlim = [1e-2, 1e2]
        if not ylim:
            ylim = [0, 100]
        ystep = pstep
        zstep = tstep

    yrange = np.arange(xlim[0], xlim[1], xstep)
    zrange = np.arange(zlim[0], zlim[1], zstep)

    plt.figure()

    xrange = [get_eos(mol=mol, t=mol.tc, v=v, eos=eos)["pressure"] for v in vls]

    for z in zrange:
        xrange = [get_eos(mol=mol, t=t, v=v, eos=eos)["pressure"] for v in vls]
        plt.semilogx(vls, p, label=eos)

    plt.axhline(y=0, color='k')
    plt.xlabel('Molar volume, $v (m^3 / mol)$')
    plt.ylabel('Pressure, $P (bar)$')
    plt.ylim(plim)
    plt.grid()
    plt.legend()
    plt.show()
