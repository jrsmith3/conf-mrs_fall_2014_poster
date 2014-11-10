# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def fermi(energy, temp, fermi_level = 0,):
    denom = 1 + np.exp( (energy - fermi_level)/(temp) )
    return 1.0/denom

class BandDiagram(object):
    """
    Generates a band diagram for plotting.
    """

    def __init__(self, temp = 1., fermi_level = 1., quasi_fermi_level = None, vbm = 0., cbm = 4., metal = False):
        self.n_points = 1000

        self.temp = temp
        self.fermi_level = fermi_level
        self.quasi_fermi_level = quasi_fermi_level
        self.vbm = vbm
        self.cbm = cbm
        self.metal = metal

    def plotfig(self, fig_height = 3, fig_width = 3):
        energy = np.linspace(-10, 10, self.n_points)

        if self.quasi_fermi_level:
            f = fermi(energy, self.temp, self.quasi_fermi_level)
        else:
            f = fermi(energy, self.temp, self.fermi_level)

        # Band structure and Fermi energy
        dist_width = np.linspace(0, 1.2, 2)

        valence_band = self.vbm * np.ones(2)
        conduct_band = self.cbm * np.ones(2)
        fermi_energy = self.fermi_level * np.ones(2)

        x_hi = 0.2
        x_lo = -1.2
        y_lo = -2.0
        y_hi = 10.0

        fig = plt.figure(figsize=(fig_height,fig_width))

        # Fermi distribution
        plt.plot(-f, energy, "r", linewidth = 2.0)

        # Band structure and Fermi energy
        if not self.metal:
            plt.plot(-dist_width, valence_band, "k",)
            plt.plot(-dist_width, conduct_band, "k",)
        plt.plot(-dist_width, fermi_energy, "k--",)
        if self.quasi_fermi_level:
            quasi_fermi_energy = self.quasi_fermi_level * np.ones(2)
            plt.plot(-dist_width, quasi_fermi_energy, "k-.",)

        # E_vac
        plt.plot([0, -0.05], [6, 6], "k",)

        # Surface
        plt.plot([0, 0], [y_lo, y_hi], "k",)

        # Limits, axes, etc.
        plt.ylim(y_lo, y_hi)
        plt.xlim(x_lo, x_hi)

        fig.axes[0].set_frame_on(False)
        fig.axes[0].xaxis.set(visible = False)
        fig.axes[0].yaxis.set(visible = False)

    def savefig(self, filename, fig_height = 3, fig_width = 3):
        self.plotfig(fig_height, fig_width)
        plt.savefig(filename, bbox_inches=0)

    def showfig(self, fig_height = 3, fig_width = 3):
        self.plotfig(fig_height, fig_width)
        plt.show()