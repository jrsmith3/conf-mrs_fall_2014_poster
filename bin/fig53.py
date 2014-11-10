# -*- coding: utf-8 -*-
import os
import inspect
from banddiagram import BandDiagram

target_dir = "build"
pwd = os.getcwd()
script_fqpn = inspect.getfile(inspect.currentframe())
script_basename = os.path.basename(script_fqpn)
script_base = os.path.splitext(script_basename)[0]
target_fqpn = os.path.join(pwd, target_dir, script_base + ".eps")

bd = BandDiagram(temp = 3., 
                 fermi_level = 1.,
                 metal = True)
bd.savefig(target_fqpn)
