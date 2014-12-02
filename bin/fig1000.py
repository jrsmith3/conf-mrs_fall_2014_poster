# -*- coding: utf-8 -*-
import os
import inspect
import numpy as np
import matplotlib.pyplot as plt
from banddiagram import Model, target_fig_fqfn, fermi
from params import band_diagram

# Location of the target directory relative to the directory in which this script is located.
target_rel_dir = "../build"
target_filename_ext = "eps"
script_fqfn = os.path.realpath(__file__)
target_fqfn = target_fig_fqfn(script_fqfn, target_rel_dir, target_filename_ext)

fermi_level = 1.
evac = fermi_level + 5.

bd = Model(temp = 1., 
           fermi_level = fermi_level,
           evac = evac,)
bd.savefig(target_fqfn, band_diagram["fig_height"], band_diagram["fig_width"])
