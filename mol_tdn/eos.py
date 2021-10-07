"""Module contain the equation of states tools."""
import numpy as np
import matplotlib.pyplot as plt  #TODO: use bokeh instead
from .get_data import R

# def get_t_boil(m,p)
# def get_p_vap(m,t)


class EosParameters:
    """Parameters for the EOS equations."""

    def __init__(self, mol, t, eos):
        """Compute temperature-only dependent parameters and define the other one to be assigned later."""
        self.eos = eos
        self.tr = t / mol.tc
        if eos == 'vdw':  # van der Waals
            self.a = 0.421875 * R**2 * mol.tc**2 / mol.pc
            self.b = 0.125 * R * mol.tc / mol.pc
            self.S = None
            self.k = 1
            self.u = 1
            self.w = 0
        elif eos == 'rk':  # Redlich - Kwong
            self.a = 0.42748 * R**2 * mol.tc**2 / mol.pc / np.sqrt(self.tr)
            self.b = 0.08664 * R * mol.tc / mol.pc
            self.S = None
            self.k = 1
            self.u = 1
            self.w = 0
        elif eos == 'rks':  # Redlich - Kwong - Soave
            self.a = 0.42748 * R**2 * mol.tc**2 / mol.pc
            self.b = 0.08664 * R * mol.tc / mol.pc
            self.S = 0.48 + 1.574 * mol.af - 0.176 * mol.af**2
            self.k = (1 + self.S * (1 - np.sqrt(self.tr)))**2
            self.u = 1
            self.w = 0
        elif eos == 'pr':  # Peng - Robbinson
            self.a = 0.45724 * R**2 * mol.tc**2 / mol.pc
            self.b = 0.07780 * R * mol.tc / mol.pc
            self.S = 0.37464 + 1.54226 * mol.af - 0.26992 * mol.af**2
            self.k = (1 + self.S * (1 - np.sqrt(self.tr)))**2
            self.u = 2
            self.w = -1

        for param in ["A", "B", "alpha", "beta", "gamma", "p", "q", "Delta"]:
            setattr(self, param, None)


def get_iphase(phi):
    """Understand if the fluid is at liquid (lower z solution) or gas (higher z solution) phase."""
    if len(phi) == 1:
        i = 0  # only one z solution (only gas or liquid possible, or supercritical)
    else:
        if phi[1] < phi[0]:
            i = 1  # gas phase
        else:
            i = 0  # liquid phase
    return i


def get_phase(mol, t, p, v):
    """Understand if the the phase is liquid (in this case could be also solid) or gas."""
    if t > mol.tc and p > mol.pc:
        phase = "supercritic"
    else:
        if not mol.vc:
            phase = "unknown"
        elif v > mol.vc:
            phase = "gas"
        else:
            phase = "liquid"
    return phase


def plot_pv(mol, t, plim=[-100, 100], vlim=[1e-1, 1e1]):  #pylint: disable=dangerous-default-value # Dangerous default value [] as argument
    """Plot the P(v) plot for different EOS."""
    vls = np.linspace(vlim[0], vlim[1], 1000)
    plt.figure()
    for eos in ['vdw', 'rk', 'rks', 'pr']:
        p = [get_eos(mol=mol, t=t, v=v, eos=eos)["pressure"] for v in vls]
        plt.semilogx(vls, p, label=eos)

    plt.axhline(y=0, color='k')
    plt.xlabel('Molar volume, $v (m^3 / mol)$')
    plt.ylabel('Pressure, $P (bar)$')
    plt.ylim(plim)
    plt.grid()
    plt.legend()
    plt.show()


def get_fz_plot(alpha, beta, gamma):  #TODO: add markers on the solution and at zero for gas id
    """Plot the cubic function f(Z) = Z^3 + alpha * Z^2 + beta * Z + gamma, with Z being the compressibility coeff.
    in a meaningful z range to observe its zero values."""
    z = np.linspace(-0.5, 1.5)
    fz = z**3 + alpha * z**2 + beta * z + gamma
    plt.figure()
    plt.plot(z, fz, color='red')
    plt.xlabel('Compressibility coefficient, $z$')
    plt.ylabel('Cubic function, $f(z)$')
    plt.axhline(y=0, color='k')
    plt.grid()
    plt.show()


def get_eos(mol, t, p=None, v=None, eos='pr', plot_fz=False):
    """EOS equations

    Parameters
    ----------
    mol: Molecule
        Molecule of the fluid.
    t: float
        Temperature (K)
    p: float
        Pressure (bar), if specified returns v and Z.
    v: float
        Molar volume (L/mol), if specified returns p.
    eos: string
        Choice of the equation of state to use:
            - 'vdw': van der Waals
            - 'rk': Redlich - Kwong
            - 'rks': Redlich - Kwong - Soave
            - 'pr': Peng - Robbinson
    plotcubic: bool
        Plot cubic polynomial in compressibility factor
    printresults: bool
    print off properties

    Returns
    -------
    Dict() of molecule properties at this T and P.
    """

    if v and p:
        raise RuntimeError("Both pressure and volume are specified: specify ONLY one!")
    if not v and not p:
        raise RuntimeError("Both pressure and volume are NOT specified: specify one!")

    ep = EosParameters(mol, t, eos)

    # If temp and vol provided, compute press
    if v and not p:
        p = R * t / (v - ep.b) - ep.a / (v**2 + ep.u * ep.b * v + ep.w * ep.b**2)

    # Compute A and B that are functions of temp and press.
    ep.A = ep.a * ep.k * p / R**2 / t**2
    ep.B = ep.b * p / R / t

    # The cubic equation z**3 + alpha *  z**2 + beta * z + gamma = 0 (z is the compressibility factor, PV=ZnRT)
    ep.alpha = -1 - ep.B + ep.u * ep.B
    ep.beta = ep.A + ep.w * ep.B**2 - ep.u * ep.B - ep.u * ep.B**2
    ep.gamma = -ep.A * ep.B - ep.w * ep.B**2 - ep.w * ep.B**3

    if plot_fz:
        get_fz_plot(ep.alpha, ep.beta, ep.gamma)

    # Rewritten as x**3 + ep.p * x + ep.q = 0, with x = z + alpha/3 ("depressed" cubic)
    ep.p = ep.beta - ep.alpha**2 / 3
    ep.q = 2 * ep.alpha**3 / 27 - ep.alpha * ep.beta / 3 + ep.gamma
    ep.Delta = ep.q**2 / 4 + ep.p**3 / 27

    if ep.Delta > 0:  # Use Cardano's solution
        x_sol = np.cbrt(-ep.q / 2 + np.sqrt(ep.Delta)) + np.cbrt(-ep.q / 2 - np.sqrt(ep.Delta))
        z_list = [x_sol - ep.alpha / 3]
    else:  # Use trigonometric solution
        z_list = []
        subeq = np.arccos(3 * ep.q / 2 / ep.p * np.sqrt(-3 / ep.p))
        for offset in [0, 1, 2]:
            x_sol = 2 * np.sqrt(-ep.p / 3) * np.cos(subeq / 3 - 2 * np.pi * offset / 3)
            z_list.append(x_sol - ep.alpha / 3)
        z_list.sort()  # [ z_liq, z_meaningless, z_vap ]
        z_list.pop(1)  # remove meaningless central value

    mdens, hr_adim, sr_adim, gr_adim, hr, sr, gr, phi = [], [], [], [], [], [], [], []
    for zsol in z_list:

        # Compute residual enthalpy (hr), entropy (sr) and Gibb's free energy (gr)
        if eos == 'vdw':  # van der Waals
            hr_adim.append(zsol - 1 - ep.A / zsol)
            sr_adim.append(np.log(zsol - ep.B))
        elif eos == 'pr':
            ecap = ep.S * np.sqrt(ep.tr / ep.k)
            subeq1 = ep.A / 2 / np.sqrt(2) / ep.B
            subeq2 = np.log((zsol + ep.B * (1 + np.sqrt(2))) / (zsol + ep.B * (1 - np.sqrt(2))))
            hr_adim.append(zsol - 1 - subeq1 * (1 + ecap) * subeq2)
            sr_adim.append(np.log(zsol - ep.B) - subeq1 * ecap * subeq2)

        gr_adim.append(hr_adim[-1] - sr_adim[-1])
        phi.append(np.exp(gr_adim[-1]))  # (-) Fugacity coefficient
        hr.append(hr_adim[-1] * R * 100 * t)  # (kJ/mol) Residual Enthalpy
        sr.append(sr_adim[-1] * R * 100)  # (kJ/mol/K) Residual Entropy
        gr.append(gr_adim[-1] * R * 100 * t)  # (kJ/mol) Residual Gibb's Free Energy
        mdens.append(p / (R * 1000 * t * zsol))  # molar density (mol/L)

    iphase = get_iphase(phi)
    if p and not v:
        v = 1.0 / mdens[iphase]
    phase = get_phase(mol, t, p, v)

    res_dict = {
        "phase": phase,
        "temperature": t,
        "temperature_unit": "K",
        "temperature_reduced": ep.tr,
        "pressure": p,
        "pressure_unit": "bar",
        "pressure_reduced": p / mol.pc,
        "molar_density": mdens[iphase],
        "molar_density_unit": "mol/L",
        "density": mdens[iphase] * mol.mm / 1000,
        "density_unit": "g/cm^3",
        "fugacity_coefficient": phi[iphase],
        "compressibility_factor": z_list[iphase],
        "fugacity": phi[iphase] * p,
        "fugaciy_unit": "bar",
        "molar_volume": v,
        "molar_volume_unit": "L/mol",
        "enthalpy_reduced": hr[iphase],
        "enthalpy_reduced_unit": "kJ/mol",
        "entropy_reduced": sr[iphase],
        "entropy_reduced_unit": "kJ/mol/K",
        "energy_gibbs_reduced": gr[iphase],
        "energy_gibbs_reduced_unit": "kJ/mol",
    }
    return res_dict


def compute_eos(mol, t, p=None, v=None, eos='pr', plot_fz=False):
    """Get first the critical volume if not computed already, then get the eos."""
    if not mol.vc or mol.vc_eos != eos:
        mol.vc_eos = eos
        mol.vc = get_eos(mol, t=mol.tc, p=mol.pc, eos=eos)['molar_volume']
    return get_eos(mol, t, p, v, eos, plot_fz)
