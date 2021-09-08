#!/usr/bin/python3

# Import all relevant modules
from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import sys
from modules.params.get_param import Params


#------------------------------#
# Variables
#------------------------------#

# Look for using default flags (uses all default values)
params = Params(len(sys.argv) > 1 and sys.argv[1].lower() == "-defaults")

# Directory paths
root_directory = params.ask("Root Directory", "../Output/Scattered/New/")
sub_directory = params.ask("Folder", "Gas")

# Set the type (Qphi or Uphi)
image_type = params.ask("Type", "PI", ["PI", "Qphi", "Uphi"])

# Set the scale (log or lin)
image_scale = params.ask("Scale", "log", ["lin", "log"])

# Set the FWHM
image_FWHM = params.ask("FWHM", 0.05)

# Set the min and max
image_vmin = params.ask("Min Flux", 1e-22)
image_vmax = params.ask("Max Flux", 1e-18)

# Add stars or not
image_plotstars = params.ask("Plot Stars", True, [True, False])

# Get the plot name
filename = root_directory + sub_directory + params.ask("Filename", "scattered.pdf")

# Add a new line
print("\n---\n")



#------------------------------#
# Creating Plots
#------------------------------#

# Import PyMCFOST
import pymcfost as mcfost

# Create the axes
fig, axes = plt.subplots()

# Get the MCFOST data
mod_cont = mcfost.Image(root_directory + sub_directory)

# Create the image
image = mod_cont.plot(
    ax = axes,
    colorbar = True,
    scale = image_scale,
    plot_stars = image_plotstars,
    type = image_type,
    psf_FWHM=image_FWHM,
    vmin = image_vmin,
    vmax = image_vmax
)


#------------------------------#
# Saving Plots
#------------------------------#

# Save the figure
plt.savefig(filename, bbox_inches='tight')

# Show the graph in an xw display window
plt.show()