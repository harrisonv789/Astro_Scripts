# Astro Scripts :star:

This repository contains all the scripts used to analyse data produced by the smoothed-particle hydrodynamics simulator, PHANTOM, which aims to reproduce positions of planets forming in proto-planetary discs. Although these scripts will not show how PHANTOM is used, all scripts here are used for my physics research project to analyse the data that was produced. The scripts use Python to convert FITS files into meaningful visualisations. :snake:

This research was conducted and completed in the Monash University (Melbourne, Australia) undergraduate Science degree (BSc) as part of an astrophysics major. These unis are PHS3350 and PHS3360. With the exception of the modules installed below, all other scripts are open-sourced and can be used and changed in the future.


## Setup :scroll:
There exists some submodules that need to be run prior to any scripts being executed here. To set up, make sure the **modules** folder exists and change into the folder.

CASA Cube can be used to plot FITS data files in python. The repository we use is from Christophe Pinté's repository and can be installed via the following steps:

```
cd modules

git clone https://github.com/cpinte/casa_cube.git
cd casa_cube
python3 setup.py install
```

Additionally, to run the radiative transfer code, **MCFOST**, we can do this through Python as well. This can be done by installing Christophe Pinté's repository for this module:


```
cd modules

git clone https://github.com/cpinte/pymcfost.git
cd pymcfost
python3 setup.py install
```