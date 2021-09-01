#!/usr/bin/python3

from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import pymcfost as mcfost
from modules.colorbar_utils import colorbar2, shift_axes




#------------------------------#
# Directory Information
#------------------------------#
# Simulation name
name = "Soft_0.1Mdisc"

# Path to the DSHARP data
dir = "../Output/Soft/MCFOST_data/{}/".format(name)

# Model directories
mod_dir_basename = dir

# Name of the output PDF file
#filename = "plots/Report{}.pdf".format(name)
filename = "{}.pdf".format(name)
#------------------------------#




#------------------------------#
# Observational Variables
#------------------------------#

# Include Observation Data
include_observation = True

# Directory to Observational Data
# Velocity CO channel must be called lines.fits.gz or lines.fits
# Continuum data must be called RT.fits.gz or RT.fits
dir_observation = dir + "DSHARP/"

# The name of the observation
obs_name = "DSHARP - IM Lupi"

# Match Observation Scales
# This will match the bmin, bmax and bpa from the observation
match_observation = True
#------------------------------#



#------------------------------#
# System Variables
#------------------------------#

# Star velocity factor moving away
v_system = 4.5

# Location of planet
# For simulations without a planet, use 0, 0
p_loc = [-0.52, 0.44]

# Location of star shift
s_shift = [0, 0]
#------------------------------#



#------------------------------#
# Model Variables
#------------------------------#

# The model names
models = ["1", "2", "3", "5", "7", "10"]

# The mass of the planets (in Jupiter masses)
# For models without planets, write 0
# MAKE SURE THE SIZE OF THIS ARRAY IS THE SAME AS MODELS
p_masses = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

# Velocity channels
v_channels = [-0.40, -1.45, -1.80, 1.35]
#------------------------------#



#------------------------------#
# Plotting Variables
#------------------------------#

# Whether to plot continuum images or not
include_continuum = True

# The colour mapping for the observational plot
cmap_cont = "gist_earth"

# Whether to use Flux Temperature or not
c_plot_temp = True

# Whether to plot the location of sinks on the data or not
plot_sinks = True

# The minimum and maximum flux value for the pixels for velocity images
# These will scale the velocity channels
v_f_min = 8
v_f_max = 60

# The f_min value for the pixels in the continuum image
# The minimum and maximum flux value for the pixels on the continuum images
# These will scale the continuum
c_f_min = 2
c_f_max = 60

# The continuum pixel addition
# This makes the continuum darker the larger the value is
# Keep this as 0 if you do not want to change the scaling
c_mod_pix_add = 0

# The continuum colour scale
# Options are 'log' or 'lin'
c_color_scale = 'lin'

# The limits of the graph
# (max_x, min_x, min_y, max_y)
limits = [1.1,-1.1,-1.1,1.1]

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

    CO =        casa.Cube(dir_observation + "lines.fits")

# Create the subplots
fig, axes = plt.subplots(
    nrows = n_models + int(include_observation),
    ncols = n_channels + int(include_continuum),
    figsize = (f_size * (n_channels + int(include_continuum)), f_size * (n_models + int(include_observation))),
    sharex='all',
    sharey='all'
)

# Add some whitespace between them
plt.subplots_adjust(wspace = f_spacing, hspace = f_spacing)

# Adjust the axes for each row
if include_continuum:
    for i in range(n_models + int(include_observation)):
        shift_axes(axes[i,0],-0.03,0)
        #shift_axes(axes[i,4:],0.01,0)

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
if len(p_masses) != len(models):
    raise Exception("Incorect Planet Masses Array Size. Make sure the array length is identical to the model array length.")




#------------------------------#
# Plot the Observational data
#------------------------------#

# If including the observational data
if include_observation:

    # If plotting continuum graphs
    if include_continuum:

        print("Plotting Observation Continuum")

        # We plot the observations on the first row
        image = cont.plot(
            colorbar = False,
            cmap = cmap_cont,
            color_scale = c_color_scale,
            ax = axes[0,0],
            no_xlabel = True,
            no_ylabel = False,
            limits = limits,
            shift_dx = s_shift[0],
            shift_dy = s_shift[1],
            Tb = c_plot_temp,
            fmin = c_f_min,
            fmax = c_f_max
        )

        # Show the colour bar in the plot
        colorbar2(image)

        # Add the planet and star to the plot
        axes[0,0].plot(s_shift[0],  s_shift[1],     "*", color="white", ms=4)
        axes[0,0].plot(p_loc[0],    p_loc[1],       "o", color="cyan",  ms=2)

        # Label the planet name on the continuum plot
        axes[0,0].text(
            0.05,
            0.9,
            obs_name,
            horizontalalignment = 'left',
            color = "white",
            transform = axes[0,0].transAxes,
            fontsize = 10
        )


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

        # Plot the continuum
        if include_observation and match_observation:
            image = mod_cont.plot(
                ax = axes[k + 1, 0],
                colorbar = False,
                bmaj = cont.bmaj,
                bmin = cont.bmin,
                bpa = cont.bpa,
                no_xlabel = no_xlabel,
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
                ax = axes[k + int(include_observation), 0],
                colorbar = False,
                no_xlabel = no_xlabel,
                limits = limits,
                cmap = cmap_cont,
                scale = c_color_scale,
                Tb = c_plot_temp,
                vmin = c_f_min,
                vmax = c_f_max,
                plot_stars = plot_sinks
            )

        # Label the model on the continuum plot
        if p_masses[k] == 0:
            mod_label = models[k] + " Model"
        else:
            mod_label = str(p_masses[k]) + ("M$_\mathrm{jup}$ %s Model" % mod)
        
        axes[k + int(include_observation), 0].text(
            0.05,
            0.9,
            mod_label,
            horizontalalignment = 'left',
            color = "white",
            transform = axes[k+int(include_observation),0].transAxes,
            fontsize = 10
        )

        # Add the planet and star to the plot
        #axes[k+int(include_observation),0].plot(s_shift[0],  s_shift[1], "*", color="white", ms=4)

        #if mplanet != 0:
        #    axes[k+int(include_observation),0].plot(p_loc[0],    p_loc[1],   "o", color="cyan",  ms=2)

        # Show the colour bar in the plot
        colorbar2(image)

    # Set the change in velocity
    delta_v = None

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
