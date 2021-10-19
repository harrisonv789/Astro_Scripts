#!/usr/bin/python3

# Import all relevant modules
from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import sys
from modules.params import Params


#------------------------------#
# Variables
#------------------------------#

# Look for using default flags (uses all default values)
params = Params()

# Directory paths
root_directory = params.get("root")
inputs = params.get_array("inputs", strings = True)

# Get whether to use CASA cube or not
use_casa = params.get("casa")
if use_casa: inputs = [params.get("dir_casa")]

# Set the type (Qphi or Uphi)
image_type = params.get("type")

# Set the scale (log or lin)
image_scale = params.get("scale")

# Set the FWHM
image_FWHM = params.get("fwhm")

# Set the min and max
image_vmin = params.get("fmin")
image_vmax = params.get("fmax")

# The limits of the graph
# (max_x, min_x, min_y, max_y)
limits_max = params.get("limits")
limits = [limits_max, -limits_max, -limits_max, limits_max]

# Map the colours to matplotlib colours
colors = {"grey": "Greys_r", "inferno": "inferno", "viridis": "viridis", "normal": "inferno", "sepia": "copper"}
cmap = colors[params.get("cmap")]

# Add stars or not
image_plotstars = params.get("stars")

# Python Figure Size
image_size = 4.0

# Whether to show the scattered light image to the screen or not
image_show = params.get("show")

# Whether to show the scattered light image to the screen or not
image_save= params.get("save")

# Get the plot name
filename = root_directory + params.get("file")



#------------------------------#
# Creating Plots
#------------------------------#

# Import PyMCFOST and CASA
import pymcfost as mcfost
from modules.casa_cube import casa_cube as casa

# Create the axes
fig, axes = plt.subplots(
    nrows = 1,
    ncols = len(inputs),
    figsize = (image_size * len(inputs), image_size),
    sharex='all',
    sharey='all'
)


# If using CASA
if use_casa:

    # Get the CASA daa
    cont =  casa.Cube(root_directory + inputs[0] + "/RT.fits")

    # Creae the image
    image = cont.plot(
        ax = axes[0,0],
        colorbar = True,
        color_scale = image_scale,
        fmin = image_vmin * 1e16,
        fmax = image_vmax * 1e16,
        cmap = cmap,
    )


# Otherwise, if using PyMCFOST
else:

    # Loop through each of the files
    for idx, data in enumerate(inputs):

        # Get the MCFOST data
        mod_cont = mcfost.Image(root_directory + data)

        # Create the image
        image = mod_cont.plot(
            title = "%s $M_\mathrm{jup}$" % data,
            ax = axes[idx],
            colorbar = idx == len(inputs) - 1,
            scale = image_scale,
            no_ylabel = idx > 0,
            limits = limits,
            plot_stars = image_plotstars,
            type = image_type,
            psf_FWHM=image_FWHM,
            vmin = image_vmin,
            vmax = image_vmax,
            cmap = cmap
        )


#------------------------------#
# Saving Plots
#------------------------------#

# Save the figure
if image_save:
    plt.savefig(filename, bbox_inches='tight')

# Show the graph in an xw display window
if image_show:
    plt.show()