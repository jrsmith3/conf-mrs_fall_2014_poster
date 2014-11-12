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
import bete
import electrode
import datac
from banddiagram import target_fig_fqfn

# Location of the target directory relative to the directory in which this script is located.
target_rel_dir = "../build"
target_filename_ext = "eps"
script_fqfn = os.path.realpath(__file__)
target_fqfn = target_fig_fqfn(script_fqfn, target_rel_dir, target_filename_ext)

# input_params = {
#     "temp": 300,
#     "barrier": 2.4,
#     "richardson": 100,
#     "beta_flux": 1e10,
#     "beta_energy": 2000, #should be 20k, but I'm adjusting for 10.1063/1.1656484
#     "beta_stop_dist": 2000,
#     "doping_conc": 1e17,
#     "surf_recomb_vel": 3e4,
#     "elec_lifetime": 0.1,
#     "elec_diff_len": 0.2,

#     "position": 0,
#     "voltage": 0,
#     "emissivity": 0.5
#     }

class f50(datac.Datac):
    def plot(self, **kwargs):
        """
        Plot figure
        """
        fig = plt.figure(**kwargs)
        plt.semilogy(self.abscissae, self.ordinates.to("A/cm2"))

        plt.ylabel("Output current density [$Acm^{-2}$]")
        plt.xlabel("Temperature [K]")
        return fig

input_params = {
    "temp": 300,
    "barrier": 2.4,
    "richardson": 100,

    # Parameters for Si
    # Schwede et.al. \cite{10.1038/nmat2814}
    "el_effective_mass": constants.m_e,
    "ho_effective_mass": 0.57 * constants.m_e, 
    "accept_conc": units.Quantity(1e19, "1/cm3"),
    # Sze & Ng \cite{9780471143239}
    "accept_ionization_energy": units.Quantity(0.044, "eV"), 
    "bandgap": 1.12, 

    "beta_flux": 1e10,
    "beta_energy": 20000,
    "ehp_efficiency": 0.1,
}

abscissae = np.linspace(300,700, 50) * units.K

data = f50(input_params, abscissae, "temp", electrode.Electrode.calc_richardson_current_density)
data.show()
