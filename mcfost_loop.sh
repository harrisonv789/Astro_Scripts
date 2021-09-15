#!/bin/bash

# This script loops through all PHANTOM dump files and creates an
#   MCFOST FITS file for each one using some command.

# Store the parameters
MCFOST_COM="/fred/oz015/cpinte/mcfost/src/mcfost"
DIRECTORY="../runs/scattered"
PARA=IM_Lup.para
PLANET_AZ=-30
WAVELENGTH=1.6
SCATTERING=-only_scatt
PREFIX=IM_Lup_0

# Remove all previous data files
if [ -d $DIRECTORY/data_$WAVELENGTH ]
then
    rm -r $DIRECTORY/data_*;
fi

# Stores the counter
NUMBER=0

# Loop through every file
for FILE in $DIRECTORY/$PREFIX*; do

    # Check if the file already exists (and skips)
    if [ ! -d $DIRECTORY/FITS_$NUMBER ];
    then

        echo -e "\033[0;36 Attempting to Convert $FILE \033[0m"

        # Create the command
        $MCFOST_COM $DIRECTORY/$PARA -phantom $FILE -planet_az $PLANET_AZ $SCATTERING -img $WAVELENGTH -root_dir $DIRECTORY;

        # Make a check to see if the file is complete
        if [ -f $DIRECTORY/data_$WAVELENGTH/RT.fits.gz ];
        then

            echo -e "\033[0;32 MCFOST Completed File $FILE \033[0m";

            # Change the file name
            mv $DIRECTORY/data_$WAVELENGTH $DIRECTORY/FITS_$NUMBER;

        # Otherwise, output failed file  
        else

            echo -e "MCFOST Failed File $FILE";
            rm -r $DIRECTORY/data_*;

        fi

    # If the file already exists
    else
        
        echo "\033[1;33 File $FILE Already Converted. \033[0m"

    fi

    # Increment the file
    ((NUMBER=NUMBER+1))

done

echo -e "\033[0;31 Completed all Files. \033[0m"
