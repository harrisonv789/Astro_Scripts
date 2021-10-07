#!/usr/bin/python3

from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import pymcfost as mcfost
from modules.colorbar_utils import colorbar2, shift_axes
from modules.params import Params


#------------------------------#
# Variables
#------------------------------#

# Set up the parameters
params = Params()



#------------------------------#
# Directory Information
#------------------------------#

# Path to the DSHARP data
dir = params.get("dir")

# Name of the simulation
name = params.get("name")

# Model directories
mod_dir_basename = dir if name.replace(" ", "") == ""else dir + name + "/"

# Name of the output PDF file
filename = mod_dir_basename + params.get("file")
#------------------------------#




#------------------------------#
# Observational Variables
#------------------------------#

# Include Observation Data
include_observation = params.get("inc_obs")

# Directory to Observational Data
# Velocity CO channel must be called lines.fits.gz or lines.fits
# Continuum data must be called RT.fits.gz or RT.fits
dir_observation = dir + "DSHARP/"

# The name of the observation
obs_name = "DSHARP - IM Lupi"

# Match Observation Scales
# This will match the bmin, bmax and bpa from the observation
match_observation = params.get("match")
#------------------------------#



#------------------------------#
# System Variables
#------------------------------#

# Star velocity factor moving away
v_system = params.get("v_sys")

# Location of planet
p_loc = params.get_array("p_loc")

# Location of star shift
s_shift = [0, 0]
#------------------------------#



#------------------------------#
# Model Variables
#------------------------------#

# The model names
models = params.get_array("models", strings = True)

# The mass of the planets (in Jupiter masses)
# For models without planets, write 0
# MAKE SURE THE SIZE OF THIS ARRAY IS THE SAME AS MODELS
p_masses = params.get_array("p_mass")

# Velocity channels
v_channels = params.get_array("v_chan")
#------------------------------#



#------------------------------#
# Plotting Variables
#------------------------------#

# Whether to plot continuum images or not
include_continuum = params.get("inc_cont")

# Whether to plot the channels or not
include_channels = params.get("inc_chan")

# The colour mapping for the observational plot
cmap_cont = "gist_earth"

# Whether to use Flux Temperature or not
c_plot_temp = True

# Whether to plot the location of sinks on the data or not
plot_sinks = params.get("plot_sinks")

# The minimum and maximum flux value for the pixels for velocity images
# These will scale the velocity channels
v_f_min = params.get("v_min")
v_f_max = params.get("v_max")

# The f_min value for the pixels in the continuum image
# The minimum and maximum flux value for the pixels on the continuum images
# These will scale the continuum
c_f_min = params.get("c_min")
c_f_max = params.get("c_max")

# The continuum pixel addition
# This makes the continuum darker the larger the value is
# Keep this as 0 if you do not want to change the scaling
c_mod_pix_add = 0

# The continuum colour scale
# Options are 'log' or 'lin'
c_color_scale = params.get("c_scale")

# The limits of the graph
# (max_x, min_x, min_y, max_y)
limits_max = params.get("limits")
limits = [limits_max,-limits_max,-limits_max,limits_max]

# Python Figure Size
f_size = 2.0

# Python spacing between figures
f_spacing = 0.12
#------------------------------#




#------------------------------#
# Applicaion Variables
# DO NOT CHANGE
#------------------------------#

# The number of models being used
n_models = len(models)

# The number of channels being used
n_channels = len(v_channels)
#------------------------------#




#------------------------------#
# Set up the Plots
#------------------------------#

# If including the observational data
if include_observation:
    # Create continuum and CO data
    if include_continuum:
        cont =  casa.Cube(dir_observation + "RT.fits")

    if include_channels:
        CO =    casa.Cube(dir_observation + "lines.fits")

# Create the subplots
if include_channels:
    fig, axes = plt.subplots(
        nrows = n_models + int(include_observation),
        ncols = (int(include_channels) * n_channels) + int(include_continuum),
        figsize = (f_size * ((int(include_channels) * n_channels) + int(include_continuum)), f_size * (n_models + int(include_observation))),
        sharex='all',
        sharey='all'
    )

# Otherwise make plots horizontal
else:
    fig, axes = plt.subplots(
        nrows = 1,
        ncols = n_models + int(include_observation),
        figsize = (f_size * (n_models + int(include_observation)), f_size * 1),
        sharex='all',
        sharey='all'
    )

# Add some whitespace between them
plt.subplots_adjust(wspace = f_spacing, hspace = f_spacing)

# Adjust the axes for each row
if include_continuum:
    for i in range(n_models + int(include_observation)):
        try:
            shift_axes(axes[i,0], -0.03, 0)
            #shift_axes(axes[i,4:],0.01,0)
        except:
            pass

#------------------------------#




#------------------------------#
# Creates a circle at the planet position on the graph
def CreateCircle ():
    return Circle(
        (p_loc[0], p_loc[1]),
        0.15,
        clip_on = False,
        zorder = 10,
        linewidth = 2,
        edgecolor = 'white',
        linestyle = ":",
        facecolor = (0, 0, 0, .0125),
        alpha = 0.3,
        fill = False
    )
#------------------------------#




#------------------------------#
# Broadcast any Errors
#------------------------------#

# Check for mismatched arrays
if len(p_masses) < len(models):
    raise Exception("Incorect Planet Masses Array Size. Make sure the array length is identical to the model array length.")




#------------------------------#
# Plot the Observational data
#------------------------------#

# If including the observational data
if include_observation:

    # If plotting continuum graphs
    if include_continuum:

        # Get axis
        axis = axes[0, 0] if include_channels else axes[0]

        print("Plotting Observation Continuum")

        # We plot the observations on the first row
        image = cont.plot(
            colorbar = False,
            cmap = cmap_cont,
            color_scale = c_color_scale,
            ax = axis,
            no_xlabel = include_channels,
            no_ylabel = False,
            limits = limits,
            shift_dx = s_shift[0],
            shift_dy = s_shift[1],
            Tb = c_plot_temp,
            fmin = c_f_min,
            fmax = c_f_max
        )

        # Show the colour bar in the plot
        if include_channels or n_models <= 1:
            colorbar2(image)

        # Add the planet and star to the plot
        axis.plot(s_shift[0],  s_shift[1],     "*", color="white", ms=4)
        axis.plot(p_loc[0],    p_loc[1],       "o", color="cyan",  ms=2)

        # Label the planet name on the continuum plot
        axis.text(
            0.05,
            0.9,
            obs_name,
            horizontalalignment = 'left',
            color = "white",
            transform = axis.transAxes,
            fontsize = 10
        )

    # If including velocity channels
    if include_channels:

        print("Plotting Observation Velocity Channels")

        # Loop though all the channels
        for i in range(n_channels):

            # Determine the current velocity for the observational data
            iv = np.abs(CO.velocity - (v_system + v_channels[i])).argmin()

            # Only show color bar in the last channel
            show_colorbar = i == n_channels - 1

            # Plot the velocity channel
            vel_im = CO.plot(
                iv = iv,  
                v0 = v_system,
                colorbar = False,
                ax = axes[0, int(include_continuum) + i],
                no_xlabel = True,
                no_ylabel = True,
                limits = limits,
                shift_dx = s_shift[0],
                shift_dy = s_shift[1],
                Tb = c_plot_temp,
                fmax = v_f_max,
                fmin = v_f_min
            )

            if show_colorbar:
                colorbar2(vel_im)

            # Add a circle where the planet is expected to be
            if plot_sinks:
                circle = CreateCircle()
                axes[0, int(include_continuum)  + i].add_artist(circle)
#------------------------------#



#------------------------------#
# Plot the Simulation Models
#------------------------------#

# Loop through each of the simulaions
for k, mod in enumerate(models):
    # Get the model directory
    mod_dir = mod_dir_basename + str(mod)

    # Print message
    print("Analysing output from {} located at:\n\t{}".format(mod, mod_dir))

    # Get the continuum and CO images
    mod_cont = mcfost.Image(mod_dir)
    mod_CO = mcfost.Line(mod_dir)

    # Determine whether to display the xlabel or not
    no_xlabel = k < n_models - 1

    # Add pixel values to the continuum image
    mod_cont.image += c_mod_pix_add * mod_cont.image[4,0,0,:,:]

    # If plotting the continuum
    if include_continuum:

        # Get axis
        axis = axes[k + int(include_observation), 0] if include_channels else axes[k + int(include_observation)]

        # Plot the continuum
        if include_observation and match_observation:
            image = mod_cont.plot(
                ax = axis,
                colorbar = False,
                bmaj = cont.bmaj,
                bmin = cont.bmin,
                bpa = cont.bpa,
                no_xlabel = no_xlabel and include_channels,
                no_ylabel = not include_channels,
                limits = limits,
                cmap = cmap_cont,
                scale = c_color_scale,
                Tb = c_plot_temp,
                vmin = c_f_min,
                vmax = c_f_max,
                plot_stars = plot_sinks,
            )
        
        # If no observational data to base scales on
        else:
            image = mod_cont.plot(
                ax = axis,
                colorbar = False,
                no_xlabel = no_xlabel and include_channels,
                no_ylabel = not include_channels,
                limits = limits,
                cmap = cmap_cont,
                scale = c_color_scale,
                Tb = c_plot_temp,
                vmin = c_f_min,
                vmax = c_f_max,
                plot_stars = plot_sinks
            )

        # Label the model on the continuum plot
        if p_masses[k] == 0 or True:
            mod_label = models[k] + " Model"
        else:
            mod_label = str(p_masses[k]) + ("M$_\mathrm{jup}$ Model")
        
        axis.text(
            0.05,
            0.9,
            mod_label,
            horizontalalignment = 'left',
            color = "white",
            transform = axis.transAxes,
            fontsize = 10
        )

        # Add the planet and star to the plot
        #axes[k+int(include_observation),0].plot(s_shift[0],  s_shift[1], "*", color="white", ms=4)

        #if mplanet != 0:
        #    axes[k+int(include_observation),0].plot(p_loc[0],    p_loc[1],   "o", color="cyan",  ms=2)

        # Show the colour bar in the plot
        if include_channels or k == n_models - 1:
            colorbar2(image)

    # Set the change in velocity
    delta_v = None

    # If including velocity channels
    if include_channels:

        # Loop through each of the channels
        for i in range(n_channels):

            # Only show color bar in the last channel
            show_colorbar = i == n_channels - 1

            # Plot the CO velocity channel
            if include_observation and match_observation:
                vel_im = mod_CO.plot_map(
                    v = v_channels[i],
                    ax = axes[k + 1, int(include_continuum) + i],
                    colorbar = False,
                    bmaj = CO.bmaj,
                    bmin = CO.bmin,
                    bpa = CO.bpa,
                    no_xlabel = no_xlabel,
                    no_ylabel = True,
                    limits = limits,
                    Tb = c_plot_temp,
                    Delta_v = delta_v,
                    fmax = v_f_max,
                    fmin = v_f_min,
                    plot_stars = plot_sinks
                )

            # If no observational data to base scales on
            else:
                vel_im = mod_CO.plot_map(
                    v = v_channels[i],
                    ax = axes[k + int(include_observation), int(include_continuum) + i],
                    colorbar = False,
                    no_xlabel = no_xlabel,
                    no_ylabel = True,
                    limits = limits,
                    Tb = c_plot_temp,
                    Delta_v = delta_v,
                    fmax = v_f_max,
                    fmin = v_f_min,
                    plot_stars = plot_sinks
                )

            # Plot the circle where the planet is expected to be
            if p_masses[k] != 0 and plot_sinks:
                circle = CreateCircle()
                axes[k + int(include_observation), int(include_continuum) + i].add_artist(circle)

            # Add in a colorbar
            if show_colorbar:
                colorbar2(vel_im)

#------------------------------#



# Save the figure
plt.savefig(filename, bbox_inches='tight')

# Show the graph in an xw display window
plt.show()
