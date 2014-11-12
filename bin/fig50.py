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
Calculates and plots the output current density vs. temperature for the parameters listed in the current commit (21f8be36) of the paper.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.units import Quantity
import tec
import bete

input_params = {
    "temp": 300,
    "barrier": 2.4,
    "richardson": 100,
    "beta_flux": 1e10,
    "beta_energy": 2000, #should be 20k, but I'm adjusting for 10.1063/1.1656484
    "beta_stop_dist": 2000,
    "doping_conc": 1e17,
    "surf_recomb_vel": 3e4,
    "elec_lifetime": 0.1,
    "elec_diff_len": 0.2,

    "position": 0,
    "voltage": 0,
    "emissivity": 0.5
    }

FIGNAME = "fig50.eps"

# Set up the electrode materials. I assume a Cs coating and parameters according to Wu & Kahn (10.1063/1.371191)
el_b = bete.Electrode(input_params)
# Adjust the barrier parameter because it is actually referring to electron affinity.
el_b["barrier"] = 0.5

# Set up the control material.
el_control = tec.Electrode(input_params)


temps = Quantity(np.linspace(300,700,100),"K")
output_current_densities = Quantity([], "A/m2")
control_output_current_densities = Quantity([],"A/m2")

for temp in temps:
    # pea bete electrode
    el_b["temp"] = temp
    output_current_density = \
        el_b.calc_beta_enhanced_saturation_current_density()

    appended_array = np.append(output_current_densities,
        output_current_density)

    output_current_densities = Quantity(appended_array,
        output_current_densities.unit)

    # "regular" electrode
    el_control["temp"] = temp
    control_output_current_density = \
        el_control.calc_saturation_current_density()

    appended_array = np.append(control_output_current_densities,
        control_output_current_density)

    control_output_current_densities = Quantity(appended_array,
        control_output_current_densities.unit)

y_unit = "A/cm2"

plt.semilogy(temps,output_current_densities.to(y_unit), "b")
plt.semilogy(temps,control_output_current_densities.to(y_unit), "r")

plt.legend(["bete","control"],loc="lower right")
plt.xlabel("Temperature " + str(temps.unit))
plt.ylabel("Current Density " + y_unit)
plt.savefig(FIGNAME, bbox_inches=0)
# plt.show()
