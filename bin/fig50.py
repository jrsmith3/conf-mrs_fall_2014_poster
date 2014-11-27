# -*- coding: utf-8 -*-
#The MIT License (MIT)

#Copyright (c) <2013> <Joshua Ryan Smith>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


"""
Calculates and plots both the beta-enhanced thermoelectron emission current density and the standard thermoelectron emission current density from an electrode held at an elevated temperature.
"""

import os
import inspect
import numpy as np
import matplotlib.pyplot as plt
from astropy import units, constants
import tec
import datac
from banddiagram import target_fig_fqfn

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
    "barrier": 2.4,
    "richardson": 100,

    # Parameters for Si
    # Schwede et.al. \cite{10.1038/nmat2814}
    "electron_effective_mass": constants.m_e.value,
    "hole_effective_mass": 0.57 * constants.m_e.value, 
    "acceptor_concentration": units.Quantity(1e19,"1/cm3"),
    # Sze & Ng \cite{9780471143239}
    "acceptor_ionization_energy": units.Quantity(0.044, "eV"),
    "bandgap": units.Quantity(1.12,"eV"),

    "beta_flux": 1e10,
    "beta_energy": 2e4,
    "ehp_efficiency": 0.1,
}

abscissae = np.linspace(300, 1000, 10) * units.K

bete_data = f50(input_params, abscissae, "temp", tec.electrode.BETE.calc_thermoelectron_current_density)
conv_data = f50(input_params, abscissae, "temp", tec.electrode.SC.calc_thermoelectron_current_density)

fig = bete_data.plot()
conv_data.plot(fig = fig)
plt.legend(("bete", "Control"), loc = "lower right")

plt.show()
