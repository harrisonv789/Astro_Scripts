#!/usr/bin/python3

from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import pymcfost as mcfost
from modules.colorbar_utils import colorbar2, shift_axes
from modules.params import get_param


#------------------------------#
# Variables
#------------------------------#

# Directory paths
directory = get_param.ask("Directory", "../Output/Scattered/")
filename = directory + get_param.ask("Filename", "scattered")

# Set the type (Qphi or Uphi)
image_type = get_param.ask("Type", "Qphi", ["Qphi", "Uphi"])

# Set the scale (log or lin)
image_scale = get_param.ask("Scale", "log", ["lin", "log"])

# Set the FWHM
image_scale = get_param.ask("FWHM", 0.05)

# Add stars or not
image_plotstars = get_param.ask("Plot Stars", True, [True, False])

# Add color bar or not
image_colorbar = get_param.ask("Color Bar", False, [True, False])


#------------------------------#
# Creating Plots
#------------------------------#

# Create the axes
fig, axes = plt.subplots()

# Get the MCFOST data
mod_cont = mcfost.Image(directory)




# Create the image
image = mod_cont.plot(
    ax = axes,
    colorbar = True,
    scale = image_scale,
    plot_stars = True,
    type = image_type,
    psf_FWHM=0.05
)

# Add the colour bar
if image_colorbar:
    colorbar2(image)



#------------------------------#
# Saving Plots
#------------------------------#

# Save the figure
plt.savefig(filename, bbox_inches='tight')

# Show the graph in an xw display window
plt.show()