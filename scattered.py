from matplotlib.patches import Circle
from modules.casa_cube import casa_cube as casa
import matplotlib.pyplot as plt
import numpy as np
import pymcfost as mcfost
from modules.colorbar_utils import colorbar2, shift_axes

# Directory paths
directory = "/Users/harrisonverrios/Documents/Uni/PHS3350/Output/Scattered/"
filename = directory + "scattered.pdf"

# Create the axes
fig, axes = plt.subplots()

# Get the MCFOST data
mod_cont = mcfost.Image(directory + "")




# Create the image
image = mod_cont.plot(
    ax = axes,
    colorbar = True,
    #no_xlabel = False,
    #limits = [2.1,-2.1,-2.1,3.1],
    #cmap = "gist_earth",
    scale = "log",
    #Tb = True,
    #vmin = 8,
    #vmax = 60,
    plot_stars = True,
    type = "Qphi", ##QPHI
    psf_FWHM=0.05
)




# Add the colour bar
#colorbar2(image)

# Save the figure
plt.savefig(filename, bbox_inches='tight')

# Show the graph in an xw display window
plt.show()