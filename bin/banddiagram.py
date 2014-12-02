# -*- coding: utf-8 -*-
import numpy as np
import inspect
import os
import matplotlib.pyplot as plt

def fermi(energy, temp, fermi_level = 0,):
    denom = 1 + np.exp( (energy - fermi_level)/(temp) )
    return 1.0/denom

def target_fig_fqfn(script_fqfn, target_rel_dir, target_filename_ext):
    """
    Fully-qualified filename of target figure

    :param str script_fqfn: Fully-qualified filename of plotting script.
    :param str target_rel_dir: Target directory for figure relative to plotting script.
    :param str target_filename_ext: Extension of figure.
    """
    script_dir_fqpn = os.path.dirname(script_fqfn)
    script_filename = os.path.basename(script_fqfn)
    script_filename_root = os.path.splitext(script_filename)[0]

    target_filename = ".".join((script_filename_root, target_filename_ext))

    target_dir_join = os.path.join(script_dir_fqpn, target_rel_dir, target_filename)
    target_dir_fqpn = os.path.abspath(target_dir_join)

    return target_dir_fqpn


class BandDiagram(object):
    """
    Generates a band diagram for plotting.
    """

    def __init__(self, temp = 1., fermi_level = 1., quasi_fermi_level = None, vbm = 0., cbm = 4., evac = 6, metal = False):
        self.n_points = 1000

        self.temp = temp
        self.fermi_level = fermi_level
        self.quasi_fermi_level = quasi_fermi_level
        self.vbm = vbm
        self.cbm = cbm
        self.evac = evac
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
        plt.plot(-f, energy, "r", linewidth = 5.0)

        # Band structure and Fermi energy
        if not self.metal:
            plt.plot(-dist_width, valence_band, "k",)
            plt.plot(-dist_width, conduct_band, "k",)
        plt.plot(-dist_width, fermi_energy, "k--",)
        if self.quasi_fermi_level:
            quasi_fermi_energy = self.quasi_fermi_level * np.ones(2)
            plt.plot(-dist_width, quasi_fermi_energy, "k-.",)

        # E_vac
        plt.plot([0, -0.05], [self.evac, self.evac], "k",)

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
