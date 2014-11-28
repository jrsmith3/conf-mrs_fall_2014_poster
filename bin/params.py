# -*- coding: utf-8 -*-
"""
Common parameters for various plots.
"""

from astropy import units

units.imperial.enable()

fig_height = units.Quantity(97.015, "mm")
fig_width = units.Quantity(97.015, "mm")

band_diagram = {"fig_height": fig_height.to("inch").value, 
                "fig_width": fig_width.to("inch").value,}


# Dimensions for bete plots
# bete_figsize = (width, height)
bete_figsize = (7, 6)
