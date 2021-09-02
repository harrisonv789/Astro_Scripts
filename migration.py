#!/usr/bin/python3

from modules import params
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
directory = params.ask("Directory", "../Output/Soft/Migration/")
filename = directory + params.ask("Filename", "migration")

# Target radius line
target_radius = params.ask("Target Radius (AU)", 117.0)

# Units of body mass
planet_units = params.ask("Units", "$M_{jup}$")

# Graph variables
title = params.ask("Title", "Planet Semi-Major Axis vs Time")


#------------------------------#


# The list of all data files - AU distances
starts = ["5_hard_0.1", "5_hard_0.01", "5_soft_0.1", "5_soft_0.01"]
colors = ["#880000", "#FF0000", "#004488", "#0088FF"]

data = {}

# Create the list of data
for start in starts:
	data[start] = np.loadtxt(directory + "{}_maxvals.out".format(start))

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Find min length of the data
min_idx = 1e10

for start in starts:
	if len(data[start]) < min_idx:
		min_idx = len(data[start])

# Plot each of the data points
for idx, start in enumerate(starts):
	# Get data
	d = data[start]
	
	r_idx = len(d[0]) - 2

	# Check for color exists
	if idx < len(colors):
		# Plot the graph with colors
		ax.plot(d[:min_idx,0], d[:min_idx,r_idx], color = colors[idx], label= start + planet_units)
	else:
		# No color preference
		ax.plot(d[:min_idx,0], d[:min_idx,r_idx], label = start + planet_units)

	

	# Plot start points excluding one
	if idx == 1:
		ax.text(d[0,0], d[0,r_idx],'  {:.1f} AU'.format(d[0,r_idx]))
	ax.plot(d[0,0], d[0,r_idx], 'o', color='black')

	# Plot end points excluding one
	if idx != 1:
		ax.text(d[min_idx - 1,0], d[min_idx - 1, r_idx],'  {:.1f} AU'.format(d[-1,r_idx]))
	ax.plot(d[min_idx - 1,0], d[min_idx - 1, r_idx], 'o', color='black')


# Add final location
x = np.linspace(0, np.max(data[starts[-1]][:,0] * 1.1), 2)
y = x * 0 + target_radius
ax.plot(x, y, label='Target Radius: %s AU' % str(target_radius), color='black', linestyle='dashed')


# Set the limits
ax.set_ylim([60, np.max(data[starts[-1]][:,r_idx]) * 1.1])
ax.set_xlim([0, np.max(data[starts[-1]][:min_idx,0]) * 1.1])
ax.set_ylabel('Orbitial Radius (AU)', fontsize=14)
ax.set_xlabel('Simulation Time (Myr)', fontsize=14)

# Show the plot
ax.legend()
ax.set_title(title, fontsize=16)

# Save the figure
fig.savefig(filename + ".pdf", bbox_inches='tight')

# Display the figure
plt.show()
