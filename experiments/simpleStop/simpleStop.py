#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on Fri May 19 13:32:08 2023
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code_10
accuracy_thresh = 0.8
missed_thresh = 0.1
maxSSD = 1000
minSSD = 0

rt_thresh = 1000
missed_response_thresh = 0.1
commision_thresh = 0.25

maxStopCorrect = 0.7
minStopCorrect = 0.3

maxStopCorrectPractice = 1
minStopCorrectPractice = 0

practiceCount = 0
practiceEnd = 0
# Run 'Before Experiment' code from code_11
accuracy_thresh = 0.8
missed_thresh = 0.1
maxSSD = 1000
minSSD = 0

rt_thresh = 1000
missed_response_thresh = 0.1
commision_thresh = 0.25

maxStopCorrect = 0.7
minStopCorrect = 0.3

maxStopCorrectPractice = 1
minStopCorrectPractice = 0

practiceCount = 0
testBeginFlag = 0


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.2'
expName = 'simplestop_skeleton'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/jahrios/Downloads/PsychoPy 2/simplestop_skeleton.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "StimSetup" ---
# Run 'Begin Experiment' code from code
#***************************

from copy import deepcopy
import random

color = 'black'
shapes = ["circle", "circle", "square", "square"]
conditions = ['go', 'go', 'stop']
totalShapesUsed = 4
numStim = 4
stopTaskTrials = 144
numStopPracTrials = 24
practice_blocks = 3
numTrialsPerBlock = 48
numTestBlocks = stopTaskTrials / numTrialsPerBlock
stopTrialList = []
stopPracTrialList = []
possible_responses = [
  ["circle", 'z'],
  ["circle", 'z'],
  ["square", 'm'],
  ["square", 'm'],
]

InitSSD = .25
SSD = InitSSD

def createTrialTypes(numTrialsPerBlock, color, shapes, conditions, totalShapesUsed):
    unique_combos = len(conditions) * totalShapesUsed

    stims = []
    for x in range(len(conditions)):
        for j in range(totalShapesUsed):
            stim = {
                'fileName': shapes[j]+color+'.png',
                'correct_response': possible_responses[j][1],
                'condition': conditions[x]
            }
            stims.append(stim)


    iterations = int(numTrialsPerBlock / unique_combos)

    final_stims = []
    for k in range(iterations):
        shuffled_stims = stims.copy()  # Make a copy of stims before shuffling
        random.shuffle(shuffled_stims)
        final_stims.append(shuffled_stims)


    res = [dictionary for sublist in final_stims for dictionary in sublist]
        
    
    return res

#***************************

# --- Initialize components for Routine "instructions" ---
instrStopText = visual.TextStim(win=win, name='instrStopText',
    text='In this task you will see shapes appear on the screen one at a time.\n\nOnly one response is correct for each shape.\n\nIf the shape is a square press the “M” key.\nIf the shape is a circle press the “Z” key.\n\nYou should respond as quickly and accurately as possible to each shape. \nOn some trials, a star will appear around the shape.  The star will appear with, or shortly after the shape appears.\nIf you see a star appear, please try your best to withhold your response on that trial.\nThe star appears on a trial, and you try your best to withhold your response, you will find that you will be able to stop sometimes but not always. \nPlease do not slow down your responses to wait for the star.  Continue to respond as quickly and accurately as possible.\nPress enter to continue.\n\n',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_2 = keyboard.Keyboard()

# --- Initialize components for Routine "practiceBlockSetup" ---

# --- Initialize components for Routine "newPracticeStim" ---

# --- Initialize components for Routine "trial" ---
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
goStim = visual.ImageStim(
    win=win,
    name='goStim', units='pix', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
goResp = keyboard.Keyboard()
stopSignal = visual.ImageStim(
    win=win,
    name='stopSignal', 
    image='stopSignal.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "feedback" ---
# Run 'Begin Experiment' code from code_4
#***************************

#message variable just needs some value at start
feedbackMessage=None

#***************************
text = visual.TextStim(win=win, name='text',
    text='',
    font='Arial',
    pos=[0, 0], height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "blank" ---
fixation_2 = visual.TextStim(win=win, name='fixation_2',
    text='+',
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# --- Initialize components for Routine "endTrial" ---

# --- Initialize components for Routine "practiceFeedback" ---
text_5 = visual.TextStim(win=win, name='text_5',
    text='',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_3 = keyboard.Keyboard()

# --- Initialize components for Routine "practiceRepeat" ---

# --- Initialize components for Routine "testInstructions" ---
key_resp = keyboard.Keyboard()
testText = visual.TextStim(win=win, name='testText',
    text='In this task you will see shapes appear on the screen one at a time.\n\nOnly one response is correct for each shape.\n\nIf the shape is a square press the “M” key.\nIf the shape is a circle press the “Z” key.\n\nYou should respond as quickly and accurately as possible to each shape. \nOn some trials, a star will appear around the shape.  The star will appear with, or shortly after the shape appears.\nIf you see a star appear, please try your best to withhold your response on that trial.\nThe star appears on a trial, and you try your best to withhold your response, you will find that you will be able to stop sometimes but not always. \nPlease do not slow down your responses to wait for the star.  Continue to respond as quickly and accurately as possible.\nPress enter to continue.\n\n',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
# Run 'Begin Experiment' code from code_5
testBlockCount = 0

# --- Initialize components for Routine "stopBlockSetup" ---

# --- Initialize components for Routine "newStopStim" ---

# --- Initialize components for Routine "trial" ---
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
goStim = visual.ImageStim(
    win=win,
    name='goStim', units='pix', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
goResp = keyboard.Keyboard()
stopSignal = visual.ImageStim(
    win=win,
    name='stopSignal', 
    image='stopSignal.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "ITI" ---
fixation_3 = visual.TextStim(win=win, name='fixation_3',
    text=None,
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# --- Initialize components for Routine "ssdChange" ---

# --- Initialize components for Routine "endOfStopBlockFeedback" ---
text_6 = visual.TextStim(win=win, name='text_6',
    text='',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_4 = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "StimSetup" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
StimSetupComponents = []
for thisComponent in StimSetupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "StimSetup" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StimSetupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "StimSetup" ---
for thisComponent in StimSetupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "StimSetup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "instructions" ---
continueRoutine = True
# update component parameters for each repeat
key_resp_2.keys = []
key_resp_2.rt = []
_key_resp_2_allKeys = []
# keep track of which components have finished
instructionsComponents = [instrStopText, key_resp_2]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "instructions" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrStopText* updates
    
    # if instrStopText is starting this frame...
    if instrStopText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instrStopText.frameNStart = frameN  # exact frame index
        instrStopText.tStart = t  # local t and not account for scr refresh
        instrStopText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrStopText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrStopText.started')
        # update status
        instrStopText.status = STARTED
        instrStopText.setAutoDraw(True)
    
    # if instrStopText is active this frame...
    if instrStopText.status == STARTED:
        # update params
        pass
    
    # *key_resp_2* updates
    waitOnFlip = False
    
    # if key_resp_2 is starting this frame...
    if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.tStart = t  # local t and not account for scr refresh
        key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_2.started')
        # update status
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_2.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_2.getKeys(keyList=['return'], waitRelease=False)
        _key_resp_2_allKeys.extend(theseKeys)
        if len(_key_resp_2_allKeys):
            key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
            key_resp_2.rt = _key_resp_2_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instructions" ---
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
practiceBlocks = data.TrialHandler(nReps=3.0, method='fullRandom', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='practiceBlocks')
thisExp.addLoop(practiceBlocks)  # add the loop to the experiment
thisPracticeBlock = practiceBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
if thisPracticeBlock != None:
    for paramName in thisPracticeBlock:
        exec('{} = thisPracticeBlock[paramName]'.format(paramName))

for thisPracticeBlock in practiceBlocks:
    currentLoop = practiceBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
    if thisPracticeBlock != None:
        for paramName in thisPracticeBlock:
            exec('{} = thisPracticeBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "practiceBlockSetup" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_7
    #***************************
    goCumRT = 0
    goRTCount = 0
    omissionCount = 0
    commissionCount = 0
    stopTrialCount = 0
    stopSuccessCount = 0
    goTrialCount = 0
    
    #***************************
    
    stopPracTrialList = createTrialTypes(numStopPracTrials, color, shapes, conditions, totalShapesUsed)
    
    thisExp.addData("stopPracTrialList", stopPracTrialList)
    
    trialCount = 0
    print(len(stopPracTrialList))
    print(stopPracTrialList)
    # keep track of which components have finished
    practiceBlockSetupComponents = []
    for thisComponent in practiceBlockSetupComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "practiceBlockSetup" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceBlockSetupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practiceBlockSetup" ---
    for thisComponent in practiceBlockSetupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "practiceBlockSetup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practiceTrials = data.TrialHandler(nReps=numStopPracTrials, method='fullRandom', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='practiceTrials')
    thisExp.addLoop(practiceTrials)  # add the loop to the experiment
    thisPracticeTrial = practiceTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
    if thisPracticeTrial != None:
        for paramName in thisPracticeTrial:
            exec('{} = thisPracticeTrial[paramName]'.format(paramName))
    
    for thisPracticeTrial in practiceTrials:
        currentLoop = practiceTrials
        # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
        if thisPracticeTrial != None:
            for paramName in thisPracticeTrial:
                exec('{} = thisPracticeTrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "newPracticeStim" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_12
        #***************************
        practiceTrials.addData("StartTrialTimeStamp", core.getTime())
        
        currentStopPracTrial = stopPracTrialList.pop(0)
        currentGoStim = currentStopPracTrial['fileName']
        currentCorrectResponse = currentStopPracTrial['correct_response']
        currentStopOrGo = currentStopPracTrial['condition']
        
        if currentStopOrGo == 'stop':
            stopSignal.opacity = 1
        elif currentStopOrGo == 'go': 
            stopSignal.opacity = 0
            
        practiceTrials.addData("trialType", currentStopOrGo)
        practiceTrials.addData("goStim", currentGoStim)
        practiceTrials.addData("correctResponse", currentCorrectResponse)
        practiceTrials.addData("ssd", SSD)
        
        SSDInput = SSD + .5 # +.5 because that's the duration of the fixation cross before the go stim appears
        
        #***************************
        # keep track of which components have finished
        newPracticeStimComponents = []
        for thisComponent in newPracticeStimComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "newPracticeStim" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in newPracticeStimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "newPracticeStim" ---
        for thisComponent in newPracticeStimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "newPracticeStim" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        goStim.setPos([0, 0])
        goStim.setImage(currentGoStim)
        goResp.keys = []
        goResp.rt = []
        _goResp_allKeys = []
        # keep track of which components have finished
        trialComponents = [fixation, goStim, goResp, stopSignal]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *goStim* updates
            
            # if goStim is starting this frame...
            if goStim.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goStim.frameNStart = frameN  # exact frame index
                goStim.tStart = t  # local t and not account for scr refresh
                goStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goStim.started')
                # update status
                goStim.status = STARTED
                goStim.setAutoDraw(True)
            
            # if goStim is active this frame...
            if goStim.status == STARTED:
                # update params
                pass
            
            # if goStim is stopping this frame...
            if goStim.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goStim.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    goStim.tStop = t  # not accounting for scr refresh
                    goStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goStim.stopped')
                    # update status
                    goStim.status = FINISHED
                    goStim.setAutoDraw(False)
            
            # *goResp* updates
            waitOnFlip = False
            
            # if goResp is starting this frame...
            if goResp.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goResp.frameNStart = frameN  # exact frame index
                goResp.tStart = t  # local t and not account for scr refresh
                goResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goResp.started')
                # update status
                goResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(goResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(goResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if goResp is stopping this frame...
            if goResp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goResp.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    goResp.tStop = t  # not accounting for scr refresh
                    goResp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goResp.stopped')
                    # update status
                    goResp.status = FINISHED
                    goResp.status = FINISHED
            if goResp.status == STARTED and not waitOnFlip:
                theseKeys = goResp.getKeys(keyList=['m', 'z'], waitRelease=False)
                _goResp_allKeys.extend(theseKeys)
                if len(_goResp_allKeys):
                    goResp.keys = _goResp_allKeys[0].name  # just the first key pressed
                    goResp.rt = _goResp_allKeys[0].rt
                    # was this correct?
                    if (goResp.keys == str(corrGoResp)) or (goResp.keys == corrGoResp):
                        goResp.corr = 1
                    else:
                        goResp.corr = 0
            
            # *stopSignal* updates
            
            # if stopSignal is starting this frame...
            if stopSignal.status == NOT_STARTED and tThisFlip >= SSDInput-frameTolerance:
                # keep track of start time/frame for later
                stopSignal.frameNStart = frameN  # exact frame index
                stopSignal.tStart = t  # local t and not account for scr refresh
                stopSignal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stopSignal, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stopSignal.started')
                # update status
                stopSignal.status = STARTED
                stopSignal.setAutoDraw(True)
            
            # if stopSignal is active this frame...
            if stopSignal.status == STARTED:
                # update params
                pass
            
            # if stopSignal is stopping this frame...
            if stopSignal.status == STARTED:
                # is it time to stop? (based on local clock)
                if tThisFlip > 1.5-frameTolerance:
                    # keep track of stop time/frame for later
                    stopSignal.tStop = t  # not accounting for scr refresh
                    stopSignal.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stopSignal.stopped')
                    # update status
                    stopSignal.status = FINISHED
                    stopSignal.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if goResp.keys in ['', [], None]:  # No response was made
            goResp.keys = None
            # was no response the correct answer?!
            if str(corrGoResp).lower() == 'none':
               goResp.corr = 1;  # correct non-response
            else:
               goResp.corr = 0;  # failed to respond (incorrectly)
        # store data for practiceTrials (TrialHandler)
        practiceTrials.addData('goResp.keys',goResp.keys)
        practiceTrials.addData('goResp.corr', goResp.corr)
        if goResp.keys != None:  # we had a response
            practiceTrials.addData('goResp.rt', goResp.rt)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.500000)
        
        # --- Prepare to start Routine "feedback" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_4
        if currentStopOrGo == 'stop' and goResp.keys is None:
            feedbackMessage = "Correct"
        else:
            feedbackMessage = "There was a star"
        
        
        if currentStopOrGo == 'go' and goResp.keys == currentCorrectResponse:
            feedbackMessage = "Correct"
        elif currentStopOrGo == 'go' and goResp.keys is None:
            feedbackMessage = "Respond Faster"
        elif currentStopOrGo == 'go' and goResp.keys != currentCorrectResponse and goResp.keys is not None:
            feedbackMessage = "Incorrect"
        
        
        text.setText(feedbackMessage)
        # keep track of which components have finished
        feedbackComponents = [text]
        for thisComponent in feedbackComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "feedback" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text* updates
            
            # if text is starting this frame...
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = t  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.started')
                # update status
                text.status = STARTED
                text.setAutoDraw(True)
            
            # if text is active this frame...
            if text.status == STARTED:
                # update params
                pass
            
            # if text is stopping this frame...
            if text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    text.tStop = t  # not accounting for scr refresh
                    text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text.stopped')
                    # update status
                    text.status = FINISHED
                    text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback" ---
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "blank" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        blankComponents = [fixation_2]
        for thisComponent in blankComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "blank" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation_2* updates
            
            # if fixation_2 is starting this frame...
            if fixation_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_2.frameNStart = frameN  # exact frame index
                fixation_2.tStart = t  # local t and not account for scr refresh
                fixation_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_2.started')
                # update status
                fixation_2.status = STARTED
                fixation_2.setAutoDraw(True)
            
            # if fixation_2 is active this frame...
            if fixation_2.status == STARTED:
                # update params
                pass
            
            # if fixation_2 is stopping this frame...
            if fixation_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_2.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_2.tStop = t  # not accounting for scr refresh
                    fixation_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_2.stopped')
                    # update status
                    fixation_2.status = FINISHED
                    fixation_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in blankComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "blank" ---
        for thisComponent in blankComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        
        # --- Prepare to start Routine "endTrial" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_13
        #***************************
        print(f'currentSSD: {SSD}')
        #Adjusting SSD within a range of 0-750ms
        if currentStopPracTrial['condition'] == 'stop':
            if goResp.keys is None:
                if SSD <= 1:
                    SSD = deepcopy(SSD)  + .05
                    print("Successful stop.")
                    print(f'adujsted SSD: {SSD}')
            else:
                if SSD > .001:
                    SSD = deepcopy(SSD)  - .05
                    print("Failed stop.")
                    print(f'adujsted SSD: {SSD}')
        
        if currentStopPracTrial['condition'] == 'go':
            goTrialCount = goTrialCount + 1
        
        if goResp.corr and currentStopPracTrial['condition'] == 'go':
            goCumRT = goCumRT + goResp.rt
            goRTCount = goRTCount + 1
        
        if currentStopPracTrial['condition'] == 'stop':
            stopTrialCount = stopTrialCount + 1
        
        if currentStopPracTrial['condition'] == 'stop' and goResp.keys is None:
            stopSuccessCount = stopSuccessCount + 1
        
        if currentStopPracTrial['condition'] == 'go':
            if goResp.keys is None:
                omissionCount = omissionCount + 1
            elif goResp.corr == 0:
                commissionCount = commissionCount + 1
        
        #Outputting a bunch of variables
        practiceTrials.addData("fixationOnset", fixation.tStart)
        practiceTrials.addData("goStimOnset", goStim.tStart)
        if SSD  != -1:
            practiceTrials.addData("stopSignalOnset", stopSignal.tStart)
        
        #***************************
        # keep track of which components have finished
        endTrialComponents = []
        for thisComponent in endTrialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "endTrial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in endTrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "endTrial" ---
        for thisComponent in endTrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from code_13
        practiceTrials.addData("EndTrialTimeStamp", core.getTime())
        # the Routine "endTrial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed numStopPracTrials repeats of 'practiceTrials'
    
    
    # --- Prepare to start Routine "practiceFeedback" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_10
    #***************************
    import numpy as np
    
    if goRTCount > 0:
        goRTFeedback = goCumRT/goRTCount
        goRTFeedback = round(goRTFeedback, 2)
    else:
        goRTFeedback = 'Null'
    
    if goTrialCount > 0:
        commissionRate = (commissionCount/goTrialCount)*100
        commissionRate = round(commissionRate, 2)
        omissionRate = (omissionCount/goTrialCount)*100
        omissionRate = round(omissionRate, 2)
    else: 
        commissionRate = 1
        omissionRate = 1
    
    if stopTrialCount > 0: 
        probabilityOfStop = stopSuccessCount/stopTrialCount
        probabilityOfStop = round(probabilityOfStop, 2)
    else:
        probabilityOfStop = 1
    
    SSDFeedback = (SSD)/2
    SSDFeedback = round(SSDFeedback, 2)
    
    stopMessage = "You have completed the practice and will now move onto the testing phase"
    stopMessage += "\nPlease take this time to read your feedback if there is any, and take a short break. Press enter to continue."
    
    practiceCount += 1
    if practiceCount == practice_blocks:
        practiceEnd = 1
    elif commissionRate > commision_thresh and probabilityOfStop < maxStopCorrectPractice and probabilityOfStop > minStopCorrectPractice:
        practiceEnd = 1
    else:
        if commissionRate > commision_thresh:
            stopMessage += "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Z key" \
                            + "\n\tSquare: M key"
                            
        if goRTFeedback != 'Null' and goRTFeedback > rt_thresh:
            stopMessage += "\nYou have been responding too slowly, please respond to each shape as quickly and as accurately as possible."
    
        if omissionRate > missed_response_thresh:
            stopMessage += "\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes."
    
        if probabilityOfStop == maxStopCorrectPractice:
            stopMessage += "\nYou have not been stopping your response when stars are present.  Please try your best to stop your response if you see a star."
        elif probabilityOfStop == minStopCorrectPractice:
            stopMessage += "\nDo not slow down and wait for the star to appear. Please respond as quickly and accurately as possible when a star does not appear."
            
    #***************************
    text_5.setText(stopMessage)
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # keep track of which components have finished
    practiceFeedbackComponents = [text_5, key_resp_3]
    for thisComponent in practiceFeedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "practiceFeedback" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_5* updates
        
        # if text_5 is starting this frame...
        if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_5.started')
            # update status
            text_5.status = STARTED
            text_5.setAutoDraw(True)
        
        # if text_5 is active this frame...
        if text_5.status == STARTED:
            # update params
            pass
        
        # *key_resp_3* updates
        waitOnFlip = False
        
        # if key_resp_3 is starting this frame...
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_3.started')
            # update status
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceFeedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practiceFeedback" ---
    for thisComponent in practiceFeedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys = None
    practiceBlocks.addData('key_resp_3.keys',key_resp_3.keys)
    if key_resp_3.keys != None:  # we had a response
        practiceBlocks.addData('key_resp_3.rt', key_resp_3.rt)
    # the Routine "practiceFeedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "practiceRepeat" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_6
    if practiceEnd == 1:
        practiceBlocks.finished = True
    # keep track of which components have finished
    practiceRepeatComponents = []
    for thisComponent in practiceRepeatComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "practiceRepeat" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceRepeatComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practiceRepeat" ---
    for thisComponent in practiceRepeatComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "practiceRepeat" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 3.0 repeats of 'practiceBlocks'


# --- Prepare to start Routine "testInstructions" ---
continueRoutine = True
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
testInstructionsComponents = [key_resp, testText]
for thisComponent in testInstructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "testInstructions" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *key_resp* updates
    waitOnFlip = False
    
    # if key_resp is starting this frame...
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp.started')
        # update status
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['return'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *testText* updates
    
    # if testText is starting this frame...
    if testText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        testText.frameNStart = frameN  # exact frame index
        testText.tStart = t  # local t and not account for scr refresh
        testText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(testText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'testText.started')
        # update status
        testText.status = STARTED
        testText.setAutoDraw(True)
    
    # if testText is active this frame...
    if testText.status == STARTED:
        # update params
        pass
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in testInstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "testInstructions" ---
for thisComponent in testInstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "testInstructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
stopBlocks = data.TrialHandler(nReps=numTestBlocks, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='stopBlocks')
thisExp.addLoop(stopBlocks)  # add the loop to the experiment
thisStopBlock = stopBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
if thisStopBlock != None:
    for paramName in thisStopBlock:
        exec('{} = thisStopBlock[paramName]'.format(paramName))

for thisStopBlock in stopBlocks:
    currentLoop = stopBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
    if thisStopBlock != None:
        for paramName in thisStopBlock:
            exec('{} = thisStopBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "stopBlockSetup" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_9
    #***************************
    
    goCumRT = 0
    goRTCount = 0
    omissionCount = 0
    commissionCount = 0
    stopTrialCount = 0
    stopSuccessCount = 0
    goTrialCount = 0
    testBlockCount += 1
    #***************************
    
    stopTrialList = createTrialTypes(numTrialsPerBlock, color, shapes, conditions, totalShapesUsed)
    
    thisExp.addData(f"Test Block: {testBlockCount}", stopTrialList)
    # keep track of which components have finished
    stopBlockSetupComponents = []
    for thisComponent in stopBlockSetupComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "stopBlockSetup" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stopBlockSetupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "stopBlockSetup" ---
    for thisComponent in stopBlockSetupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "stopBlockSetup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    testTrials = data.TrialHandler(nReps=numTrialsPerBlock, method='fullRandom', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='testTrials')
    thisExp.addLoop(testTrials)  # add the loop to the experiment
    thisTestTrial = testTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
    if thisTestTrial != None:
        for paramName in thisTestTrial:
            exec('{} = thisTestTrial[paramName]'.format(paramName))
    
    for thisTestTrial in testTrials:
        currentLoop = testTrials
        # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
        if thisTestTrial != None:
            for paramName in thisTestTrial:
                exec('{} = thisTestTrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "newStopStim" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_14
        #***************************
        testTrials.addData("StartTrialTimeStamp", core.getTime())
        
        currentStopTestTrial = stopTrialList.pop(0)
        currentGoStim = currentStopTestTrial['fileName']
        currentCorrectResponse = currentStopTestTrial['correct_response']
        currentStopOrGo = currentStopTestTrial['condition']
        currentSSD = SSD
        
        if currentStopOrGo == 'stop':
            stopSignal.opacity = 1
        elif currentStopOrGo == 'go': 
            stopSignal.opacity = 0
            
        testTrials.addData("trialType", currentStopOrGo)
        testTrials.addData("goStim", currentGoStim)
        testTrials.addData("correctResponse", currentCorrectResponse)
        testTrials.addData("ssd", SSD)
        
        SSDInput = SSD + .5 # +.5 because that's the duration of the fixation cross before the go stim appears
        
        #***************************
        # keep track of which components have finished
        newStopStimComponents = []
        for thisComponent in newStopStimComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "newStopStim" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in newStopStimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "newStopStim" ---
        for thisComponent in newStopStimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "newStopStim" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        goStim.setPos([0, 0])
        goStim.setImage(currentGoStim)
        goResp.keys = []
        goResp.rt = []
        _goResp_allKeys = []
        # keep track of which components have finished
        trialComponents = [fixation, goStim, goResp, stopSignal]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *goStim* updates
            
            # if goStim is starting this frame...
            if goStim.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goStim.frameNStart = frameN  # exact frame index
                goStim.tStart = t  # local t and not account for scr refresh
                goStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goStim.started')
                # update status
                goStim.status = STARTED
                goStim.setAutoDraw(True)
            
            # if goStim is active this frame...
            if goStim.status == STARTED:
                # update params
                pass
            
            # if goStim is stopping this frame...
            if goStim.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goStim.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    goStim.tStop = t  # not accounting for scr refresh
                    goStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goStim.stopped')
                    # update status
                    goStim.status = FINISHED
                    goStim.setAutoDraw(False)
            
            # *goResp* updates
            waitOnFlip = False
            
            # if goResp is starting this frame...
            if goResp.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goResp.frameNStart = frameN  # exact frame index
                goResp.tStart = t  # local t and not account for scr refresh
                goResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goResp.started')
                # update status
                goResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(goResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(goResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if goResp is stopping this frame...
            if goResp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goResp.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    goResp.tStop = t  # not accounting for scr refresh
                    goResp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goResp.stopped')
                    # update status
                    goResp.status = FINISHED
                    goResp.status = FINISHED
            if goResp.status == STARTED and not waitOnFlip:
                theseKeys = goResp.getKeys(keyList=['m', 'z'], waitRelease=False)
                _goResp_allKeys.extend(theseKeys)
                if len(_goResp_allKeys):
                    goResp.keys = _goResp_allKeys[0].name  # just the first key pressed
                    goResp.rt = _goResp_allKeys[0].rt
                    # was this correct?
                    if (goResp.keys == str(corrGoResp)) or (goResp.keys == corrGoResp):
                        goResp.corr = 1
                    else:
                        goResp.corr = 0
            
            # *stopSignal* updates
            
            # if stopSignal is starting this frame...
            if stopSignal.status == NOT_STARTED and tThisFlip >= SSDInput-frameTolerance:
                # keep track of start time/frame for later
                stopSignal.frameNStart = frameN  # exact frame index
                stopSignal.tStart = t  # local t and not account for scr refresh
                stopSignal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stopSignal, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stopSignal.started')
                # update status
                stopSignal.status = STARTED
                stopSignal.setAutoDraw(True)
            
            # if stopSignal is active this frame...
            if stopSignal.status == STARTED:
                # update params
                pass
            
            # if stopSignal is stopping this frame...
            if stopSignal.status == STARTED:
                # is it time to stop? (based on local clock)
                if tThisFlip > 1.5-frameTolerance:
                    # keep track of stop time/frame for later
                    stopSignal.tStop = t  # not accounting for scr refresh
                    stopSignal.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stopSignal.stopped')
                    # update status
                    stopSignal.status = FINISHED
                    stopSignal.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if goResp.keys in ['', [], None]:  # No response was made
            goResp.keys = None
            # was no response the correct answer?!
            if str(corrGoResp).lower() == 'none':
               goResp.corr = 1;  # correct non-response
            else:
               goResp.corr = 0;  # failed to respond (incorrectly)
        # store data for testTrials (TrialHandler)
        testTrials.addData('goResp.keys',goResp.keys)
        testTrials.addData('goResp.corr', goResp.corr)
        if goResp.keys != None:  # we had a response
            testTrials.addData('goResp.rt', goResp.rt)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.500000)
        
        # --- Prepare to start Routine "ITI" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        ITIComponents = [fixation_3]
        for thisComponent in ITIComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ITI" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation_3* updates
            
            # if fixation_3 is starting this frame...
            if fixation_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_3.frameNStart = frameN  # exact frame index
                fixation_3.tStart = t  # local t and not account for scr refresh
                fixation_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_3.started')
                # update status
                fixation_3.status = STARTED
                fixation_3.setAutoDraw(True)
            
            # if fixation_3 is active this frame...
            if fixation_3.status == STARTED:
                # update params
                pass
            
            # if fixation_3 is stopping this frame...
            if fixation_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_3.tStartRefresh + 1.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_3.tStop = t  # not accounting for scr refresh
                    fixation_3.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_3.stopped')
                    # update status
                    fixation_3.status = FINISHED
                    fixation_3.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ITIComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ITI" ---
        for thisComponent in ITIComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.500000)
        
        # --- Prepare to start Routine "ssdChange" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_3
        #***************************
        
        #Adjusting SSD within a range of 0-750ms
        if currentStopTestTrial['condition'] == 'stop':
            if goResp.keys is None:
                if SSD <= 1:
                    SSD = deepcopy(SSD)  + .05
            else:
                if SSD > .001:
                    SSD = deepcopy(SSD)  - .05
        
        if currentStopTestTrial['condition'] == 'go':
            goTrialCount = goTrialCount + 1
        
        if goResp.corr and currentStopTestTrial['condition'] == 'go':
            goCumRT = goCumRT + goResp.rt
            goRTCount = goRTCount + 1
        
        if currentStopTestTrial['condition'] == 'stop':
            stopTrialCount = stopTrialCount + 1
        
        if currentStopTestTrial['condition'] == 'stop' and goResp.keys is None:
            stopSuccessCount = stopSuccessCount + 1
        
        if currentStopTestTrial['condition'] == 'go':
            if goResp.keys is None:
                omissionCount = omissionCount + 1
            elif goResp.corr == 0:
                commissionCount = commissionCount + 1
        
        #Outputting a bunch of variables
        testTrials.addData("fixationOnset", fixation.tStart)
        testTrials.addData("goStimOnset", goStim.tStart)
        if SSD  != -1:
            testTrials.addData("stopSignalOnset", stopSignal.tStart)
        
        #***************************
        # keep track of which components have finished
        ssdChangeComponents = []
        for thisComponent in ssdChangeComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ssdChange" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ssdChangeComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ssdChange" ---
        for thisComponent in ssdChangeComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from code_3
        #***************************
        
        testTrials.addData("EndingSSD", SSD)
        testTrials.addData("EndTrialTimeStamp", core.getTime())
        
        #***************************
        # the Routine "ssdChange" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed numTrialsPerBlock repeats of 'testTrials'
    
    
    # --- Prepare to start Routine "endOfStopBlockFeedback" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_11
    #***************************
    
    if goRTCount > 0:
        goRTFeedback = goCumRT/goRTCount
        goRTFeedback = round(goRTFeedback, 2)
    else:
        goRTFeedback = 'Null'
    
    if goTrialCount > 0:
        commissionRate = (commissionCount/goTrialCount)*100
        commissionRate = round(commissionRate, 2)
        omissionRate = (omissionCount/goTrialCount)*100
        omissionRate = round(omissionRate, 2)
    else: 
        commissionRate = 'Null'
        omissionRate = 'Null'
    
    if stopTrialCount > 0: 
        probabilityOfStop = stopSuccessCount/stopTrialCount
        probabilityOfStop = round(probabilityOfStop, 2)
    else:
        probabilityOfStop = 'Null'
    
    SSDFeedback = (SSD)/2
    SSDFeedback = round(SSDFeedback, 2)
    
    stopMessage = "You have completed the practice and will now move onto the testing phase"
    stopMessage += "\nPlease take this time to read your feedback if there is any, and take a short break. Press enter to continue."
    
    practiceCount += 1
    if practiceCount == practice_blocks:
        testBeginFlag = 1
    elif commissionRate > commision_thresh and probabilityOfStop < maxStopCorrectPractice and probabilityOfStop > minStopCorrectPractice:
        testBeginFlag = 1
    else:
        if commissionRate > commision_thresh:
            stopMessage += "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Z key" \
                            + "\n\tSquare: M key"
                            
        if goRTFeedback > rt_thresh:
            stopMessage += "\nYou have been responding too slowly, please respond to each shape as quickly and as accurately as possible."
    
        if omissionRate > missed_response_thresh:
            stopMessage += "\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes."
    
        if probabilityOfStop == maxStopCorrectPractice:
            stopMessage += "\nYou have not been stopping your response when stars are present.  Please try your best to stop your response if you see a star."
        elif probabilityOfStop == minStopCorrectPractice:
            stopMessage += "\nDo not slow down and wait for the star to appear. Please respond as quickly and accurately as possible when a star does not appear."
            
    #***************************
    text_6.setText(stopMessage)
    key_resp_4.keys = []
    key_resp_4.rt = []
    _key_resp_4_allKeys = []
    # keep track of which components have finished
    endOfStopBlockFeedbackComponents = [text_6, key_resp_4]
    for thisComponent in endOfStopBlockFeedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "endOfStopBlockFeedback" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_6* updates
        
        # if text_6 is starting this frame...
        if text_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_6.frameNStart = frameN  # exact frame index
            text_6.tStart = t  # local t and not account for scr refresh
            text_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_6.started')
            # update status
            text_6.status = STARTED
            text_6.setAutoDraw(True)
        
        # if text_6 is active this frame...
        if text_6.status == STARTED:
            # update params
            pass
        
        # *key_resp_4* updates
        waitOnFlip = False
        
        # if key_resp_4 is starting this frame...
        if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_4.frameNStart = frameN  # exact frame index
            key_resp_4.tStart = t  # local t and not account for scr refresh
            key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_4.started')
            # update status
            key_resp_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_4.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_4.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_4_allKeys.extend(theseKeys)
            if len(_key_resp_4_allKeys):
                key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in endOfStopBlockFeedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "endOfStopBlockFeedback" ---
    for thisComponent in endOfStopBlockFeedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_4.keys in ['', [], None]:  # No response was made
        key_resp_4.keys = None
    stopBlocks.addData('key_resp_4.keys',key_resp_4.keys)
    if key_resp_4.keys != None:  # we had a response
        stopBlocks.addData('key_resp_4.rt', key_resp_4.rt)
    # the Routine "endOfStopBlockFeedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed numTestBlocks repeats of 'stopBlocks'


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()