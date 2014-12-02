# -*- coding: utf-8 -*-
"""
Calculates beta-enhanced thermoelectron emission at various values of incident beta flux. Also calculates thermoelectron emission from a semiconductor experiencing no beta irradiation.
"""

import os
import inspect
import numpy as np
import matplotlib.pyplot as plt
from astropy import units, constants
import tec
import datac
from banddiagram import target_fig_fqfn
from params import bete_figsize

# Location of the target directory relative to the directory in which this script is located.
target_rel_dir = "../build"
target_filename_ext = "eps"
script_fqfn = os.path.realpath(__file__)
target_fqfn = target_fig_fqfn(script_fqfn, target_rel_dir, target_filename_ext)

class f50(datac.Datac):
    def plot(self, fig = None, **kwargs):
        """
        Plot figure
        """
        if not fig:
            fig = plt.figure(**kwargs)
        plt.semilogy(self.abscissae, self.ordinates.to("A/cm2"))

        plt.ylabel("Output current density [$Acm^{-2}$]")
        plt.xlabel("Temperature [K]")
        return fig

input_params = {
    "temp": 300.,
    "barrier": 1.4,
    "richardson": 100,

    # Parameters for Si
    # Schwede et.al. \cite{10.1038/nmat2814}
    "electron_effective_mass": constants.m_e.value,
    "hole_effective_mass": 0.57 * constants.m_e.value, 
    "acceptor_concentration": units.Quantity(1e19,"1/cm3"),
    # Sze & Ng \cite{9780471143239}
    "acceptor_ionization_energy": units.Quantity(0.044, "eV"),
    "bandgap": units.Quantity(1.12,"eV"),

    "beta_flux": 1e8,
    "beta_energy": 2e4,
    "ehp_efficiency": 0.1,
}

# Calculate data
# ==============
abscissae = np.linspace(300, 600, 10) * units.K
beta_fluxes = np.logspace(8, 10, 3) / (units.s * units.cm**2)

bete_electrodes = []

for beta_flux in beta_fluxes:
    input_params["beta_flux"] = beta_flux

    bete_electrode = f50(input_params, abscissae, "temp", tec.electrode.BETE.calc_thermoelectron_current_density)

    bete_electrodes.append(bete_electrode)

sc_electrode = f50(input_params, abscissae, "temp", tec.electrode.SC.calc_thermoelectron_current_density)


# Plot data
# =========
fig = bete_electrodes[0].plot(None, figsize = bete_figsize)

for bete_electrode in bete_electrodes[1:]:
    bete_electrode.plot(fig = fig)

sc_electrode.plot(fig = fig)

labels = ["{0:.3g}".format(beta_flux) for beta_flux in beta_fluxes] + ["control"]
plt.legend(labels, loc = "lower right")
plt.title("Adjust beta flux, $\Phi$")
# plt.show()
plt.savefig(target_fqfn)
