# IMPORTANT
# Run this script like casa -c moment_9_creation.py
import shutil, os

# Get the directory information
directory = '../Output/S2_Final/Moment/'
infile = directory + 'pseudo_casa.fits'
outfile_1 = directory + 'pseudo_casa_M1.fits'
outfile_9 = directory + 'pseudo_casa_M9.fits'
momentfile = directory + "IM_Lupi_casa"

# Difine the moment parameters
moments=[1, 9]
axis='spectral'
excludepix=[-0.007, 0.0022]

# Remove the outfiles that exist
try:
    shutil.rmtree(momentfile + ".maximum_coord")
    shutil.rmtree(momentfile + ".weighted_coord")
except OSError:
    pass

# Export the file images
immoments(imagename=infile, moments=moments, axis=axis, excludepix=excludepix, outfile=momentfile)
exportfits(imagename=momentfile + '.weighted_coord', fitsimage=outfile_1, overwrite=True)
exportfits(imagename=momentfile + '.maximum_coord', fitsimage=outfile_9, overwrite=True)

# Remove log file
os.system("rm casa*.log")
os.system("rm *.last")

# Print the complete information
print("Moment 9 file complete in %s%s." % (directory, outfile_9))