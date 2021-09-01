#!/usr/bin/python3

from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import pymcfost as mcfost
from modules.colorbar_utils import colorbar2, shift_axes




#------------------------------#
# Variables
#------------------------------#

# Set the type (Qphi or Uphi)
image_type = "Qphi"

# Set the scale (log or lin)
image_scale = "log"

# Add color bar or not
image_colorbar = False

# Directory paths
directory = "../Output/Scattered/"
filename = directory + "scattered.pdf"



#------------------------------#
# Creating Plots
#------------------------------#

# Create the axes
fig, axes = plt.subplots()

# Get the MCFOST data
mod_cont = mcfost.Image(directory + "")




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