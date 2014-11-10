# -*- coding: utf-8 -*-
import os
import inspect
from banddiagram import BandDiagram

# Location of the target directory relative to the directory in which this script is located.
target_rel_dir = "../build"
target_filename_ext = "eps"
script_fqfn = os.path.realpath(__file__)
target_fqfn = target_fig_fqfn(script_fqfn, target_rel_dir, target_filename_ext)

bd = BandDiagram(temp = 1., 
                 fermi_level = 1.,
                 metal = True)
bd.savefig(target_fqpn)
