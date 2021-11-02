import pymcfost
from multiprocessing import Pool
import os, shutil

# Define the directory
directory = '../Output/S2_Final/Moment/'
filename = 'pseudo_casa.fits'

# Define the parameters of the simulated data model
Delta_v = None
iTrans = 0
bmaj = 0.15
bmin = 0.15
bpa = -38

# Create a list model using the Moment data
model = pymcfost.Line('../Output/S2_Final/Moment/')
model.P.mol.nv = model.nv/2

# Define CPUS
num_cpu = 4 # int(os.environ['SLURM_NTASKS'])*int(os.environ['SLURM_CPUS_PER_TASK'])
pool = Pool(num_cpu)

# These arguments can be added online with a forked branch from pymcfost
# SNR=5, 
#   pool=pool
pymcfost.pseudo_CASA_simdata(model, Delta_v=Delta_v, iTrans=iTrans, bmaj=bmaj, bmin=bmin, bpa=bpa, subtract_cont=True)

# Move the file from the directory
os.remove(directory + filename)
shutil.move("CASA/" + filename, directory)
os.rmdir("CASA")

# Print the complete information
print("Noise Data Complete on Line Data. Moved to %s%s." % (directory, filename))