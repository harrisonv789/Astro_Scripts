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

If running on another computer (such as a SuperComputer) without super user access (**sudo**), then install the script using the following line:
```
python3 setyp.py install --user
```


Additionally, to run the radiative transfer code, **MCFOST**, we can do this through Python as well. This can be done by installing Christophe Pinté's repository for this module:


```
cd modules

git clone https://github.com/cpinte/pymcfost.git
cd pymcfost
python3 setup.py install
```


I have also developed my own parameter system. This allows for user-editing script parameters and being able to change inputs without editing the scripts. This is a new package and still a work-in-progress. All parameters can be found in the [SCRIPT].para files located in this repository.

```
cd modules

git clone https://github.com/harrisonv789/params.git
```

Finally, here are some python packages that must be installed:

```
pip3 install matplotlib
pip3 install numpy
```