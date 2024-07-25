# Shared Control Project Repo

## Description
This project is looking to see the effects of shared control on stop inhibition by creating an experiment 
which has the user control the height of a {} by using a pressure sensitive keyboard.

## Contents of repo:
The key components of this repo include:
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


## To run Shared Control task:
`cd path/to/SharedControl`

`python experiment_FINAL.py`

## To run Simple Stop Task:
Install PsychoPy GUI and click/run simpleStop.psyexp

## Directories

notebooks: contains various notebooks used in testing task functions or analyzing the data

- tweak_SSD_sampler.ipynb: Contains testing of the SSD sample function used within the SharedControl task.
- stop_signal_test.ipynb: Contains testing of the createTrialTypes function used in the ssimple stop task
- analysis/shared_control_analysis.ipynb: This is the main analysis notebook for SharedControl data where we operationalize various variables such as the point of inhibition outlined in our preregestration
- analysis/simple_stop_qc.ipynb: This is our qc notebook for simple stop data. This notebook will output several qc metrics such as rt/acc/ssd/ssrt
- analysis/survey_analysis.ipynb: This notebook computes the survey scores for the AI survey.
- analysis/point_of_inhibition_analysis_outdated.ipynb: This notebook is currently outdated, but was our initial attempt to operationalize the point of inhbition within our pilot data prior to our preregestration.
- analysis/shared_control_trial_analysis.ipynb: Plots single trials of shared control data for qc reasons of pilot data. This was used in writing the preregestration.


old script: contains older versions of the simple stop and shared control task
simpleStop: contains the psychopy version of simple stop
