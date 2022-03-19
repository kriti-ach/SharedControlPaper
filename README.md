# Shared Control Project Repo

## Description
This project is looking to see the effects of shared control on stop inhibition by creating an experiment 
which has the user control the height of a {} by using a pressure sensitive keyboard.

## Contents of repo:
The key components of this repor include:
<ul>
    <li>experiment.py - the main experiment script to run the task</li>
    <li>wooting_utils.py - contains the keyboard specific utility functions</li>
    <li>schematics.py - not relevent, i believe this is a test verison or unfinished verison of exp</li>
    <li>tweak_SSD_sampler.ipynb - notebook running simulations to test sample_SSD funciton in exp file</li>
</ul>
## To setup keyboard:
    1. Follow the Wooting [quickstart guide](https://wooting.io/quickstart).
    2. Install appropriate dynamic libraries (dylibs). 
    
        2.1 install [libusb](https://libusb.info/):
            `brew install libusb` 

        2.2 install [hidapi](https://formulae.brew.sh/formula/hidapi):
            `brew install hidapi` 
    
        2.3 install [Wooting Analog SDK](https://github.com/WootingKb/wooting-analog-sdk):
            `brew install wootingkb/wooting/wooting-analog-sdk`
or follow the instructions for manual installation on the Github Readme linked above.


## To run task:
`cd path/to/SharedControl`

`python experiment.py`
