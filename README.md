# Shared Control Paper Repo

## Description
This project is looking to see the effects of sharing control with an aritificial intelligence (AI) agent on response inhibition by creating an experiment 
which has the user control the movement of a dot inside a ring by using a pressure sensitive keyboard. You will need a Wooting 60HE keyboard to run this experiment.

## Installation and Running Notebooks
Clone the repository using:

```bash
git clone https://github.com/kriti-a567/SharedControlPaper.git
```

Go into the repo using:

```bash
cd /path/to/SharedControlPaper
```

Generate the virtual environment and open the project in Jupyter Lab:

```bash
source setup_env.sh
```

## Running Notebooks

Select the `notebooks` directory.

Select `sharedcontrolpaper` as the Kernel in the top right corner of the screen and run notebooks.

If running the notebooks in VSCode, just select `sharedcontrolpaper` from the root directory as the kernel.

## Repository Structure

- /data:  
    - /experiment:  
      * Contains CSV files for the 'final' subjects for both the force-sensitive stopping task ('shared_control') and the simple stop task ('simple_stop'). Also contains .yml files to describe the structure of the files.
    - /surveys:  
      * Contains CSV files for the 'final' subjects for the AI trust survey. Also contains .yml files to describe the structure of the files.
- /experiments:  
    - forceSensitiveStoppingTask
        * [wooting_utils.py]: Contains the keyboard specific utility functions.
        * [forceSensitiveStoppingTask.py]: The script to run the force-sensitive stopping task.
        * /dylibs: The libraries needed to run forceSensitiveStoppingTask.py. 
    - /simpleStop  
        * The script to run the simple stop task along with relevant images etc.  
- /figures:  
    - Contains the figures in the paper. Note: Figures 1a and 1b were not generated with code and are not in this repository.  
- /notebooks:  
    - The notebooks which run through the processing and analysis.  
    - The notebooks are numbered in the order in which they should be run.  
- /src:    
    - /sharedcontrolpaper:
        * [force_sensitive_stopping_task_utils.py]: Helper functions to condense force sensitive stopping task analysis in notebooks.  
        * [simple_stop_utils.py]: Helper functions to condense simple stop analysis in notebooks.  
        * [preprocessing.py]: Run this script to preprocess data if you acquire any new data.
- /tables:  
    - Contains the tables in the paper.

## Running the force-sensitive stopping task:

Note: You will need the Wooting keyboard to run [forceSensitiveStoppingTask.py](experiments/forceSensitiveStoppingTask.py).

1. Follow the Wooting [quickstart guide](https://wooting.io/quickstart).
2. 
```bash
cd SharedControlPaper/experiments/forceSensitiveStoppingTask
```
3. Install appropriate dynamic libraries (dylibs). 

    2.1 install [libusb](https://libusb.info/):
            `brew install libusb` 

    2.2 install [hidapi](https://formulae.brew.sh/formula/hidapi):
            `brew install hidapi` 
    
    2.3 install [Wooting Analog SDK](https://github.com/WootingKb/wooting-analog-sdk):
            `brew install wootingkb/wooting/wooting-analog-sdk`

or follow the instructions for manual installation on the Github Readme linked above.
4. Run [forceSensitiveStoppingTask.py] using the PsychoPy GUI: https://www.psychopy.org/download.html.

## Running the simple stop task:

Install PsychoPy GUI: https://www.psychopy.org/download.html and click/run simpleStop.psyexp.

## To preprocess newly acquired data:

Run this script:
```bash
python src/sharedcontrolpaper/preprocessing.py
```

