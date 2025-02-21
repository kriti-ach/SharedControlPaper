# Shared Control Paper Repo

## Description
This project is looking to see the effects of sharing control with an aritificial intelligence (AI) agent on response inhibition by creating an experiment 
which has the user control the movement of a dot inside a ring by using a pressure sensitive keyboard. You will need a Wooting 60HE keyboard to run this experiment.

## Installation and Running Notebooks
Clone the repository using:

```
git clone https://github.com/kriti-a567/SharedControlPaper.git
```
Go into the repo using:

```
cd SharedControlPaper
```
Generate the `.venv` and open Jupyter Lab:
```
sh setup_env.sh
```

## Running Notebooks

Select `notebooks`.

Select `sharedcontrolpaper` as the Kernel in the top right corner of the screen.

Run all cells.

Repeat this process for every Jupyter Notebook. 

If running the notebooks in VSCode, just select `sharedcontrolpaper` from the root directory as the kernel.

## Repository Structure

- /data:  
    - /experiment:  
      * Contains CSV files for the 'final' and 'pilot' subjects for both the force-sensitive stopping task ('shared_control') and the simple stop task ('simple_stop').  
    - /surveys:  
      * Contains CSV files for the 'final' and 'pilot' subjects for both the AI trust survey and the demographics survey.  
- /experiments:  
    - forceSensitiveStoppingTask.py  
        * The script to run the force-sensitive stopping task.   
    - /simpleStop  
        * The scripts to run the simple stop task.  
        * Install PsychoPy GUI and click/run simpleStop.psyexp.  
- /figures:  
    - Contains the figures in the paper. Note: Figures 1a and 1b were not generated with code and are not in this repository.  
- /libs/dylibs:  
    - Contains dylibs you will need to install to run the force-sensitive stopping task.  
- /notebooks:  
    - The notebooks which run through the processing and analysis.  
    - The notebooks are numbered in the order in which they should be run.  
- /src/sharedcontrolpaper:    
    - utils.py: Helper functions to condense analysis in notebooks  
    - wooting_utils.py: Contains the keyboard specific utility functions  
- /tables:  
    - Contains the tables in the paper.

## To setup keyboard (note: you will need the Wooting keyboard to run `forceSensitiveStoppingTask.py`):
1. Follow the Wooting [quickstart guide](https://wooting.io/quickstart).
2. Install appropriate dynamic libraries (dylibs). 

    2.1 install [libusb](https://libusb.info/):
            `brew install libusb` 

    2.2 install [hidapi](https://formulae.brew.sh/formula/hidapi):
            `brew install hidapi` 
    
    2.3 install [Wooting Analog SDK](https://github.com/WootingKb/wooting-analog-sdk):
            `brew install wootingkb/wooting/wooting-analog-sdk`

or follow the instructions for manual installation on the Github Readme linked above.

