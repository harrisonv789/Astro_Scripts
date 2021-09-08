#!/usr/bin/python3

# Include all relevant packages and modules
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
directory = params.ask("Directory", "../Output/New_Soft/Migration/")

# Number of files to use
starts = ["1", "2", "3", "5", "7", "10"]
file_count = params.ask("Number of Files", len(starts))

# Loop through the number of files
del starts[file_count:]
for file_idx in range(file_count):
	if file_idx < len(starts):
		starts[file_idx] = params.ask("File Name [%d]" % file_idx, starts[file_idx])
	else:
		starts.append(params.ask("File Name [%d]" % file_idx, "maxvals"))

# Whether to plot all start points
plot_startpoints = params.ask("Plot All Start Points", False)

# Whether to plot all end points
plot_endpoints = params.ask("Plot All End Points", True)

# Target radius line
target_radius = params.ask("Target Radius (AU)", 117.0)

# Minimum Plot Y-Axis
min_yaxis = params.ask("Minimum Y-Axis (AU)", 60)

# Units of body mass
planet_units = params.ask("Units", "$M_{jup}$")

# Graph variables
title = params.ask("Title", "Planet Semi-Major Axis vs Time")

# The name of the file
filename = directory + params.ask("Filename", "migration")

#------------------------------#



# Fix any variables if required
if directory[-1] != "/":
	directory += "/"


# The list of all data files - AU distances
colors = []

data = {}

# Create the list of data
for start in starts:
	# Attempt to get the data
	try:
		data[start] = np.loadtxt(directory + "{}.out".format(start))
	except:
		print("Missing data: %s%s.out" % (directory, start))
		starts.remove(start)

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

	

	# Plot only one start point (if flagged)
	if idx == 0 or plot_startpoints:
		ax.text(d[0,0], d[0,r_idx],'  {:.1f} AU'.format(d[0,r_idx]))

	ax.plot(d[0,0], d[0,r_idx], 'o', color='black')

	# Plot end points excluding one (if flagged)
	if idx == 0 or plot_endpoints:
		ax.text(d[min_idx - 1,0], d[min_idx - 1, r_idx],'  {:.1f} AU'.format(d[min_idx - 1,r_idx]))
	
	ax.plot(d[min_idx - 1,0], d[min_idx - 1, r_idx], 'o', color='black')


# Add final location
x = np.linspace(0, np.max(data[starts[-1]][:,0] * 1.1), 2)
y = x * 0 + target_radius
ax.plot(x, y, label='Target Radius: %s AU' % str(target_radius), color='black', linestyle='dashed')


# Set the limits
ax.set_ylim([min_yaxis, np.max(data[starts[-1]][:,r_idx]) * 1.1])
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
