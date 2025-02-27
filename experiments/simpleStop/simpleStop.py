#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.2),
    on Wed Jul 24 16:50:40 2024
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import prefs
from psychopy import gui, visual, core, data, logging
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)

from numpy.random import random, randint
import os  # handy system and path functions
import random

import psychopy.iohub as io
from psychopy.hardware import keyboard

from copy import deepcopy

prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'

# Run 'Before Experiment' code from practice_block_feedback
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
# Run 'Before Experiment' code from test_block_feedback

maxSSD = 1
minSSD = 0

rt_thresh = 1000
missed_response_thresh = 0.1
commision_thresh = 0.25

maxStopCorrect = 0.7
minStopCorrect = 0.3


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
if not dlg.OK:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/poldracklab/Documents/jahrios/SharedControl/Code/SharedControl/simpleStop/simpleStop_lastrun.py',
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
    size=[2560, 1440], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] is not None:
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

# --- Initialize components for Routine "start" ---
welcome = visual.TextStim(win=win, name='welcome',
    text='Welcome to the task!\n\nPress enter to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.045, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0)
start_exp = keyboard.Keyboard()

# --- Initialize components for Routine "StimSetup" ---
# Run 'Begin Experiment' code from stim_setup
#***************************

color = 'black'
shapes = ["circle", "circle", "square", "square"]
conditions = ['go', 'go', 'stop']
totalShapesUsed = 4
numStim = 4
stopTaskTrials = 144
numStopPracTrials = 24
practice_blocks = 3
numTrialsPerBlock = 48
numTestBlocks = int(stopTaskTrials / numTrialsPerBlock)
stopTrialList = []
stopPracTrialList = []
possible_responses = [
  ["circle", 'left'],
  ["circle", 'left'],
  ["square", 'right'],
  ["square", 'right'],
]

InitSSD = .35
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

stopPracTrialList = createTrialTypes(numStopPracTrials, color, shapes, conditions, totalShapesUsed)

thisExp.addData("stopPracTrialList", stopPracTrialList)

# --- Initialize components for Routine "instructions" ---
instrStopText = visual.TextStim(win=win, name='instrStopText',
    text='In this task you will see shapes appear on the screen one at a time.\n\nOnly one response is correct for each shape.\n\nIf the shape is a circle press the index finger.\nIf the shape is a square press the middle finger.\n\nYou should respond as quickly and accurately as possible to each shape.\n\nOn some trials, a star will appear around the shape.  The star can appear with, or shortly after the shape appears.\n\nIf you see a star appear, please try your best to withhold your response on that trial. If the star appears on a trial, and you try your best to withhold your response, you will find that you will be able to stop sometimes but not always.\n\nPlease do not slow down your responses to wait for the star to appear.  Continue to respond as quickly and accurately as possible.\n\nWe will start the practice when you finish the instructions. Please make sure you understand the rules before moving on. During practice, you will see a reminder of the rules in the top left of the screen and receive feedback on your performance. This will be removed for test.\n\nPress enter to continue.\n\n',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)
start_prac = keyboard.Keyboard()

# --- Initialize components for Routine "practiceBlockSetup" ---
# Run 'Begin Experiment' code from practice_block
block = 1


# --- Initialize components for Routine "newPracticeStim" ---

# --- Initialize components for Routine "trial" ---
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)
goStim = visual.ImageStim(
    win=win,
    name='goStim', units='pix', 
    image='sin', mask=None, anchor='center',
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
rules = visual.TextStim(win=win, name='rules',
    text='Circle: Index Finger\nSquare: Middle Finger\nDo not respond if a star appears!',
    font='Open Sans',
    pos=(-.6, .4), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

# --- Initialize components for Routine "feedback" ---
# Run 'Begin Experiment' code from practice_feedback
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
    depth=-1.0)
rules_2 = visual.TextStim(win=win, name='rules_2',
    text='Circle: Index Finger\nSquare: Middle Finger\nDo not respond if a star appears!',
    font='Open Sans',
    pos=(-.6, .4), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0)

# --- Initialize components for Routine "endTrial" ---

# --- Initialize components for Routine "practiceFeedback" ---
text_5 = visual.TextStim(win=win, name='text_5',
    text='',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0)
key_resp_3 = keyboard.Keyboard()

# --- Initialize components for Routine "practiceRepeat" ---

# --- Initialize components for Routine "testInstructions" ---
key_resp = keyboard.Keyboard()
testText = visual.TextStim(win=win, name='testText',
    text='We will now begin the testing phase. To summarize the instructions.\n\nIf the shape is a circle press Index Finger.\nIf the shape is a square press Middle Finger.\n\nYou should respond as quickly and accurately as possible to each shape.\n \nOn some trials, a star will appear around the shape. If you see a star appear, please try your best to withhold your response on that trial.\n\nPlease do not slow down your responses to wait for the star to appear.  You should respond as quickly and accurately as possible as soon as you see the shapes appear on the screen.\n\nPress enter to start the testing.\n\n',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0)
# Run 'Begin Experiment' code from test_setup
testBlockCount = 0
stopTrialList = createTrialTypes(numTrialsPerBlock, color, shapes, conditions, totalShapesUsed)

thisExp.addData("Test Block: 1", stopTrialList)

# --- Initialize components for Routine "stopBlockSetup" ---

# --- Initialize components for Routine "newStopStim" ---

# --- Initialize components for Routine "test_trial" ---
test_fixation = visual.TextStim(win=win, name='test_fixation',
    text='+',
    font='Arial',
    pos=[0, 0], height=.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)
goStim_test = visual.ImageStim(
    win=win,
    name='goStim_test', units='pix', 
    image='sin', mask=None, anchor='center',
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
goResp_test = keyboard.Keyboard()
stopSignal_test = visual.ImageStim(
    win=win,
    name='stopSignal_test', 
    image='stopSignal.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "ssdChange" ---

# --- Initialize components for Routine "endOfStopBlockFeedback" ---
text_6 = visual.TextStim(win=win, name='text_6',
    text='',
    font='Arial',
    pos=[0, 0], height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0)
key_resp_4 = keyboard.Keyboard()

# --- Initialize components for Routine "end" ---
ending_text = visual.TextStim(win=win, name='ending_text',
    text='Thanks for completing this task!\nPress enter to end.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0)
end_resp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "start" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
start_exp.keys = []
start_exp.rt = []
_start_exp_allKeys = []
# keep track of which components have finished
startComponents = [welcome, start_exp]
for thisComponent in startComponents:
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

# --- Run Routine "start" ---
while continueRoutine and routineTimer.getTime() < 300.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *welcome* updates
    if welcome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        welcome.frameNStart = frameN  # exact frame index
        welcome.tStart = t  # local t and not account for scr refresh
        welcome.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(welcome, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'welcome.started')
        welcome.setAutoDraw(True)
    if welcome.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > welcome.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            welcome.tStop = t  # not accounting for scr refresh
            welcome.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcome.stopped')
            welcome.setAutoDraw(False)
    
    # *start_exp* updates
    waitOnFlip = False
    if start_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_exp.frameNStart = frameN  # exact frame index
        start_exp.tStart = t  # local t and not account for scr refresh
        start_exp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_exp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'start_exp.started')
        start_exp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(start_exp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(start_exp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if start_exp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_exp.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            start_exp.tStop = t  # not accounting for scr refresh
            start_exp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_exp.stopped')
            start_exp.status = FINISHED
    if start_exp.status == STARTED and not waitOnFlip:
        theseKeys = start_exp.getKeys(keyList=['return'], waitRelease=False)
        _start_exp_allKeys.extend(theseKeys)
        if len(_start_exp_allKeys):
            start_exp.keys = _start_exp_allKeys[-1].name  # just the last key pressed
            start_exp.rt = _start_exp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "start" ---
for thisComponent in startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if start_exp.keys in ['', [], None]:  # No response was made
    start_exp.keys = None
thisExp.addData('start_exp.keys',start_exp.keys)
if start_exp.keys is not None:  # we had a response
    thisExp.addData('start_exp.rt', start_exp.rt)
thisExp.nextEntry()
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-300.000000)

# --- Prepare to start Routine "StimSetup" ---
continueRoutine = True
routineForceEnded = False
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
routineForceEnded = False
# update component parameters for each repeat
start_prac.keys = []
start_prac.rt = []
_start_prac_allKeys = []
# keep track of which components have finished
instructionsComponents = [instrStopText, start_prac]
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
while continueRoutine and routineTimer.getTime() < 180.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrStopText* updates
    if instrStopText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instrStopText.frameNStart = frameN  # exact frame index
        instrStopText.tStart = t  # local t and not account for scr refresh
        instrStopText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrStopText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrStopText.started')
        instrStopText.setAutoDraw(True)
    if instrStopText.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > instrStopText.tStartRefresh + 180-frameTolerance:
            # keep track of stop time/frame for later
            instrStopText.tStop = t  # not accounting for scr refresh
            instrStopText.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrStopText.stopped')
            instrStopText.setAutoDraw(False)
    
    # *start_prac* updates
    waitOnFlip = False
    if start_prac.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_prac.frameNStart = frameN  # exact frame index
        start_prac.tStart = t  # local t and not account for scr refresh
        start_prac.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_prac, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'start_prac.started')
        start_prac.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(start_prac.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(start_prac.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if start_prac.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_prac.tStartRefresh + 180-frameTolerance:
            # keep track of stop time/frame for later
            start_prac.tStop = t  # not accounting for scr refresh
            start_prac.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_prac.stopped')
            start_prac.status = FINISHED
    if start_prac.status == STARTED and not waitOnFlip:
        theseKeys = start_prac.getKeys(keyList=['return'], waitRelease=False)
        _start_prac_allKeys.extend(theseKeys)
        if len(_start_prac_allKeys):
            start_prac.keys = _start_prac_allKeys[-1].name  # just the last key pressed
            start_prac.rt = _start_prac_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
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
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-180.000000)

# set up handler to look after randomisation of conditions etc
practiceBlocks = data.TrialHandler(nReps=3.0, method='fullRandom', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='practiceBlocks')
thisExp.addLoop(practiceBlocks)  # add the loop to the experiment
thisPracticeBlock = practiceBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
if thisPracticeBlock is not None:
    for paramName in thisPracticeBlock:
        exec('{} = thisPracticeBlock[paramName]'.format(paramName))

for thisPracticeBlock in practiceBlocks:
    currentLoop = practiceBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
    if thisPracticeBlock is not None:
        for paramName in thisPracticeBlock:
            exec('{} = thisPracticeBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "practiceBlockSetup" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from practice_block
    #***************************
    goCumRT = 0
    goRTCount = 0
    omissionCount = 0
    commissionCount = 0
    stopTrialCount = 0
    stopSuccessCount = 0
    goTrialCount = 0
    
    #***************************
    trialCount = 0
    phase = "practice"
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
    practiceTrials = data.TrialHandler(nReps=6.0, method='fullRandom', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('condition.xlsx'),
        seed=None, name='practiceTrials')
    thisExp.addLoop(practiceTrials)  # add the loop to the experiment
    thisPracticeTrial = practiceTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
    if thisPracticeTrial is not None:
        for paramName in thisPracticeTrial:
            exec('{} = thisPracticeTrial[paramName]'.format(paramName))
    
    for thisPracticeTrial in practiceTrials:
        currentLoop = practiceTrials
        # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
        if thisPracticeTrial is not None:
            for paramName in thisPracticeTrial:
                exec('{} = thisPracticeTrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "newPracticeStim" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from practice_stims
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
        routineForceEnded = False
        # update component parameters for each repeat
        goStim.setPos([0, 0])
        goStim.setImage(currentGoStim)
        goResp.keys = []
        goResp.rt = []
        _goResp_allKeys = []
        # keep track of which components have finished
        trialComponents = [fixation, goStim, goResp, stopSignal, rules]
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
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                fixation.setAutoDraw(True)
            if fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    fixation.setAutoDraw(False)
            
            # *goStim* updates
            if goStim.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goStim.frameNStart = frameN  # exact frame index
                goStim.tStart = t  # local t and not account for scr refresh
                goStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goStim, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goStim.started')
                goStim.setAutoDraw(True)
            if goStim.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goStim.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    goStim.tStop = t  # not accounting for scr refresh
                    goStim.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goStim.stopped')
                    goStim.setAutoDraw(False)
            
            # *goResp* updates
            waitOnFlip = False
            if goResp.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goResp.frameNStart = frameN  # exact frame index
                goResp.tStart = t  # local t and not account for scr refresh
                goResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goResp.started')
                goResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(goResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(goResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if goResp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goResp.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    goResp.tStop = t  # not accounting for scr refresh
                    goResp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goResp.stopped')
                    goResp.status = FINISHED
            if goResp.status == STARTED and not waitOnFlip:
                theseKeys = goResp.getKeys(keyList=['left', 'right'], waitRelease=False)
                _goResp_allKeys.extend(theseKeys)
                if len(_goResp_allKeys):
                    goResp.keys = _goResp_allKeys[0].name  # just the first key pressed
                    goResp.rt = _goResp_allKeys[0].rt
                    # was this correct?
                    if (goResp.keys == str(currentCorrectResponse)) or (goResp.keys == currentCorrectResponse):
                        goResp.corr = 1
                    else:
                        goResp.corr = 0
            
            # *stopSignal* updates
            if stopSignal.status == NOT_STARTED and tThisFlip >= SSDInput-frameTolerance:
                # keep track of start time/frame for later
                stopSignal.frameNStart = frameN  # exact frame index
                stopSignal.tStart = t  # local t and not account for scr refresh
                stopSignal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stopSignal, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stopSignal.started')
                stopSignal.setAutoDraw(True)
            if stopSignal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stopSignal.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    stopSignal.tStop = t  # not accounting for scr refresh
                    stopSignal.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stopSignal.stopped')
                    stopSignal.setAutoDraw(False)
            
            # *rules* updates
            if rules.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rules.frameNStart = frameN  # exact frame index
                rules.tStart = t  # local t and not account for scr refresh
                rules.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rules, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rules.started')
                rules.setAutoDraw(True)
            if rules.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > rules.tStartRefresh + 2.5-frameTolerance:
                    # keep track of stop time/frame for later
                    rules.tStop = t  # not accounting for scr refresh
                    rules.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rules.stopped')
                    rules.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
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
            if str(currentCorrectResponse).lower() == 'none':
               goResp.corr = 1  # correct non-response
            else:
               goResp.corr = 0  # failed to respond (incorrectly)
        # store data for practiceTrials (TrialHandler)
        practiceTrials.addData('goResp.keys',goResp.keys)
        practiceTrials.addData('goResp.corr', goResp.corr)
        if goResp.keys is not None:  # we had a response
            practiceTrials.addData('goResp.rt', goResp.rt)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from practice_feedback
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
        feedbackComponents = [text, rules_2]
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
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text* updates
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = t  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.started')
                text.setAutoDraw(True)
            if text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    text.tStop = t  # not accounting for scr refresh
                    text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text.stopped')
                    text.setAutoDraw(False)
            
            # *rules_2* updates
            if rules_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rules_2.frameNStart = frameN  # exact frame index
                rules_2.tStart = t  # local t and not account for scr refresh
                rules_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rules_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rules_2.started')
                rules_2.setAutoDraw(True)
            if rules_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > rules_2.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    rules_2.tStop = t  # not accounting for scr refresh
                    rules_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rules_2.stopped')
                    rules_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
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
            routineTimer.addTime(-0.500000)
        
        # --- Prepare to start Routine "endTrial" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from practice_trial_end
        #***************************
        print(f'practice currentSSD: {SSD}')
        #Adjusting SSD within a range of 0-1s
        if currentStopPracTrial['condition'] == 'stop':
            if goResp.keys is None:
                if SSD <= 0.95:
                    SSD = round(deepcopy(SSD)  + .05, 2)
                    print("Successful stop.")
                    print(f'practice adujsted SSD: {SSD}')
            else:
                if SSD >= .05:
                    SSD = round(deepcopy(SSD)  - .05, 2)
                    print("Failed stop.")
                    print(f'practice adujsted SSD: {SSD}')
        
        if currentStopPracTrial['condition'] == 'go':
            goTrialCount = goTrialCount + 1
        
        if goResp.keys == currentCorrectResponse and currentStopPracTrial['condition'] == 'go':
            goCumRT = goCumRT + goResp.rt
            goRTCount = goRTCount + 1
        
        if currentStopPracTrial['condition'] == 'stop':
            stopTrialCount = stopTrialCount + 1
        
        if currentStopPracTrial['condition'] == 'stop' and goResp.keys is None:
            stopSuccessCount = stopSuccessCount + 1
        
        if currentStopPracTrial['condition'] == 'go':
            if goResp.keys is None:
                omissionCount = omissionCount + 1
                print(f'{omissionCount}')
            elif goResp.keys != currentCorrectResponse:
                commissionCount = commissionCount + 1
                print(f'{commissionCount}')
            else:
                print("practice wasnt omission or comission! yay.")
        
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
        # Run 'End Routine' code from practice_trial_end
        practiceTrials.addData("EndTrialTimeStamp", core.getTime())
        practiceTrials.addData("Phase", phase)
        practiceTrials.addData("Block", block)
        # the Routine "endTrial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 6.0 repeats of 'practiceTrials'
    
    
    # --- Prepare to start Routine "practiceFeedback" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from practice_block_feedback
    #***************************
    
    if goRTCount > 0:
        goRTFeedback = goCumRT/goRTCount
        goRTFeedback = round(goRTFeedback, 2)
    else:
        goRTFeedback = 'Null'
    
    if goTrialCount > 0:
        commissionRate = (commissionCount/goTrialCount)
        print(f'comissionCount: {commissionCount}')
        print(f'goTrialCount: {goTrialCount}')
        commissionRate = round(commissionRate, 2)
        omissionRate = (omissionCount/goTrialCount)
        omissionRate = round(omissionRate, 2)
        print(f'omissionCount: {omissionCount}')
    else: 
        commissionRate = 1
        omissionRate = 1
    
    if stopTrialCount > 0: 
        probabilityOfStop = stopSuccessCount/stopTrialCount
        probabilityOfStop = round(probabilityOfStop, 2)
    else:
        probabilityOfStop = 1
    
    SSDFeedback = SSD
    SSDFeedback = round(SSDFeedback, 2)
    
    print(f'comission_rate: {commissionRate}, omission_rate: {omissionRate}')
    
    stopMessage = "\nPlease take this time to read your feedback if there is any, and take a short (1 minute) break. Press enter to continue.\n"
    
    practiceCount += 1
    block += 1
    if practiceCount == practice_blocks:
        practiceEnd = 1
        stopMessage = "Done with this practice.\nPress enter to continue."
    elif commissionRate <= commision_thresh and probabilityOfStop < maxStopCorrectPractice and probabilityOfStop > minStopCorrectPractice:
        practiceEnd = 1
        stopMessage = "Done with this practice.\nPress enter to continue."
    
    else:
        stopMessage = "Redoing this practice.\n"
    
        if commissionRate > commision_thresh:
            stopMessage += "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Index Finger" \
                            + "\n\tSquare: Middle Finger"
                            
        if goRTFeedback != 'Null' and goRTFeedback > rt_thresh:
            stopMessage += "\n\nYou have been responding too slowly, please respond to each shape as quickly and as accurately as possible."
    
        if omissionRate > missed_response_thresh:
            if commissionRate > commision_thresh:
                stopMessage += "\n\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes."
            else:
                stopMessage += "\n\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes." \
                            + "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Index Finger" \
                            + "\n\tSquare: Middle Finger"
    
        if probabilityOfStop == minStopCorrectPractice:
            stopMessage += "\n\nYou have not been stopping your response when stars are present.  Please try your best to stop your response if you see a star."
        elif probabilityOfStop == maxStopCorrectPractice:
            stopMessage += "\n\nDo not slow down and wait for the star to appear. Please respond as quickly and accurately as possible when a star does not appear."
        
        stopMessage += "\nPress enter to continue"
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
    while continueRoutine and routineTimer.getTime() < 60.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_5* updates
        if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_5.started')
            text_5.setAutoDraw(True)
        if text_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_5.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                text_5.tStop = t  # not accounting for scr refresh
                text_5.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_5.stopped')
                text_5.setAutoDraw(False)
        
        # *key_resp_3* updates
        waitOnFlip = False
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_3.started')
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_3.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_3.tStop = t  # not accounting for scr refresh
                key_resp_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_3.stopped')
                key_resp_3.status = FINISHED
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
    if key_resp_3.keys is not None:  # we had a response
        practiceBlocks.addData('key_resp_3.rt', key_resp_3.rt)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-60.000000)
    
    # --- Prepare to start Routine "practiceRepeat" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from practice_block_loop
    stopPracTrialList = createTrialTypes(numStopPracTrials, color, shapes, conditions, totalShapesUsed)
    
    thisExp.addData("stopPracTrialList", stopPracTrialList)
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
routineForceEnded = False
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# Run 'Begin Routine' code from test_setup
phase = "test"
block = 1
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
while continueRoutine and routineTimer.getTime() < 300.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp.started')
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_resp.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            key_resp.tStop = t  # not accounting for scr refresh
            key_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.stopped')
            key_resp.status = FINISHED
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['return'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *testText* updates
    if testText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        testText.frameNStart = frameN  # exact frame index
        testText.tStart = t  # local t and not account for scr refresh
        testText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(testText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'testText.started')
        testText.setAutoDraw(True)
    if testText.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > testText.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            testText.tStop = t  # not accounting for scr refresh
            testText.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'testText.stopped')
            testText.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
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
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-300.000000)

# set up handler to look after randomisation of conditions etc
stopBlocks = data.TrialHandler(nReps=numTestBlocks, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='stopBlocks')
thisExp.addLoop(stopBlocks)  # add the loop to the experiment
thisStopBlock = stopBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
if thisStopBlock is not None:
    for paramName in thisStopBlock:
        exec('{} = thisStopBlock[paramName]'.format(paramName))

for thisStopBlock in stopBlocks:
    currentLoop = stopBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
    if thisStopBlock is not None:
        for paramName in thisStopBlock:
            exec('{} = thisStopBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "stopBlockSetup" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from test_block_vars
    #***************************
    
    goCumRT = 0
    goRTCount = 0
    omissionCount = 0
    commissionCount = 0
    stopTrialCount = 0
    stopSuccessCount = 0
    goTrialCount = 0
    #***************************
    
    
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
    testTrials = data.TrialHandler(nReps=12.0, method='fullRandom', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('condition.xlsx'),
        seed=None, name='testTrials')
    thisExp.addLoop(testTrials)  # add the loop to the experiment
    thisTestTrial = testTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
    if thisTestTrial is not None:
        for paramName in thisTestTrial:
            exec('{} = thisTestTrial[paramName]'.format(paramName))
    
    for thisTestTrial in testTrials:
        currentLoop = testTrials
        # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
        if thisTestTrial is not None:
            for paramName in thisTestTrial:
                exec('{} = thisTestTrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "newStopStim" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from test_stims
        #***************************
        testTrials.addData("StartTrialTimeStamp", core.getTime())
        
        currentStopTestTrial = stopTrialList.pop(0)
        currentGoStim = currentStopTestTrial['fileName']
        currentCorrectResponse = currentStopTestTrial['correct_response']
        currentStopOrGo = currentStopTestTrial['condition']
        currentSSD = SSD
        
        if currentStopOrGo == 'stop':
            stopSignal_test.opacity = 1
        elif currentStopOrGo == 'go': 
            stopSignal_test.opacity = 0
            
        testTrials.addData("trialType", currentStopOrGo)
        testTrials.addData("goStim", currentGoStim)
        testTrials.addData("correctResponse", currentCorrectResponse)
        testTrials.addData("ssd", currentSSD)
        
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
        
        # --- Prepare to start Routine "test_trial" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        goStim_test.setPos([0, 0])
        goStim_test.setImage(currentGoStim)
        goResp_test.keys = []
        goResp_test.rt = []
        _goResp_test_allKeys = []
        # keep track of which components have finished
        test_trialComponents = [test_fixation, goStim_test, goResp_test, stopSignal_test]
        for thisComponent in test_trialComponents:
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
        
        # --- Run Routine "test_trial" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *test_fixation* updates
            if test_fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_fixation.frameNStart = frameN  # exact frame index
                test_fixation.tStart = t  # local t and not account for scr refresh
                test_fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_fixation.started')
                test_fixation.setAutoDraw(True)
            if test_fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > test_fixation.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    test_fixation.tStop = t  # not accounting for scr refresh
                    test_fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'test_fixation.stopped')
                    test_fixation.setAutoDraw(False)
            
            # *goStim_test* updates
            if goStim_test.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goStim_test.frameNStart = frameN  # exact frame index
                goStim_test.tStart = t  # local t and not account for scr refresh
                goStim_test.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goStim_test, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goStim_test.started')
                goStim_test.setAutoDraw(True)
            if goStim_test.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goStim_test.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    goStim_test.tStop = t  # not accounting for scr refresh
                    goStim_test.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goStim_test.stopped')
                    goStim_test.setAutoDraw(False)
            
            # *goResp_test* updates
            waitOnFlip = False
            if goResp_test.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                goResp_test.frameNStart = frameN  # exact frame index
                goResp_test.tStart = t  # local t and not account for scr refresh
                goResp_test.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(goResp_test, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'goResp_test.started')
                goResp_test.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(goResp_test.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(goResp_test.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if goResp_test.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > goResp_test.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    goResp_test.tStop = t  # not accounting for scr refresh
                    goResp_test.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goResp_test.stopped')
                    goResp_test.status = FINISHED
            if goResp_test.status == STARTED and not waitOnFlip:
                theseKeys = goResp_test.getKeys(keyList=['left', 'right'], waitRelease=False)
                _goResp_test_allKeys.extend(theseKeys)
                if len(_goResp_test_allKeys):
                    goResp_test.keys = _goResp_test_allKeys[0].name  # just the first key pressed
                    goResp_test.rt = _goResp_test_allKeys[0].rt
                    # was this correct?
                    if (goResp_test.keys == str(currentCorrectResponse)) or (goResp_test.keys == currentCorrectResponse):
                        goResp_test.corr = 1
                    else:
                        goResp_test.corr = 0
            
            # *stopSignal_test* updates
            if stopSignal_test.status == NOT_STARTED and tThisFlip >= SSDInput-frameTolerance:
                # keep track of start time/frame for later
                stopSignal_test.frameNStart = frameN  # exact frame index
                stopSignal_test.tStart = t  # local t and not account for scr refresh
                stopSignal_test.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stopSignal_test, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stopSignal_test.started')
                stopSignal_test.setAutoDraw(True)
            if stopSignal_test.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stopSignal_test.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    stopSignal_test.tStop = t  # not accounting for scr refresh
                    stopSignal_test.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stopSignal_test.stopped')
                    stopSignal_test.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in test_trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "test_trial" ---
        for thisComponent in test_trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if goResp_test.keys in ['', [], None]:  # No response was made
            goResp_test.keys = None
            # was no response the correct answer?!
            if str(currentCorrectResponse).lower() == 'none':
               goResp_test.corr = 1  # correct non-response
            else:
               goResp_test.corr = 0  # failed to respond (incorrectly)
        # store data for testTrials (TrialHandler)
        testTrials.addData('goResp_test.keys',goResp_test.keys)
        testTrials.addData('goResp_test.corr', goResp_test.corr)
        if goResp_test.keys is not None:  # we had a response
            testTrials.addData('goResp_test.rt', goResp_test.rt)
        # the Routine "test_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "ssdChange" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        # Run 'Begin Routine' code from ssd_staircase
        #***************************
        print(f'test current SSD: {SSD}')
        #Adjusting SSD within a range of 0-1s
        if currentStopTestTrial['condition'] == 'stop':
            print(currentStopTestTrial['condition'])
            if goResp_test.keys is None:
                if SSD <= 0.95:
                    SSD = round(deepcopy(SSD)  + .05, 2)
                    print("Successful stop wtf.")
                    print(f'test adujsted SSD: {SSD}')
            else:
                if SSD >= 0.05:
                    SSD = round(deepcopy(SSD)  - .05, 2)
                    print("Failed stop wtf.")
                    print(f'test adujsted SSD: {SSD}')
                
        
        if currentStopTestTrial['condition'] == 'go':
            goTrialCount = goTrialCount + 1
        
        if goResp_test.keys == currentCorrectResponse and currentStopTestTrial['condition'] == 'go':
            goCumRT = goCumRT + goResp_test.rt
            goRTCount = goRTCount + 1
        
        if currentStopTestTrial['condition'] == 'stop':
            stopTrialCount = stopTrialCount + 1
        
        if currentStopTestTrial['condition'] == 'stop' and goResp_test.keys is None:
            stopSuccessCount = stopSuccessCount + 1
            
        print('goResp_test.corr: goResp_test.corr')
        
        if currentStopTestTrial['condition'] == 'go':
            if goResp_test.keys is None:
                omissionCount = omissionCount + 1
            elif goResp_test.keys != currentCorrectResponse:
                commissionCount = commissionCount + 1
        
        #Outputting a bunch of variables
        testTrials.addData("fixationOnset", test_fixation.tStart)
        testTrials.addData("goStimOnset", goStim_test.tStart)
        if currentStopTestTrial['condition'] == 'stop':
            testTrials.addData("stopSignalOnset", stopSignal_test.tStart)
        
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
        # Run 'End Routine' code from ssd_staircase
        #***************************
        
        testTrials.addData("EndingSSD", SSD)
        testTrials.addData("EndTrialTimeStamp", core.getTime())
        
        testTrials.addData("Block", block)
        testTrials.addData("Phase", phase)
        #***************************
        # the Routine "ssdChange" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 12.0 repeats of 'testTrials'
    
    
    # --- Prepare to start Routine "endOfStopBlockFeedback" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from test_block_feedback
    #***************************
    
    if goRTCount > 0:
        goRTFeedback = goCumRT/goRTCount
        goRTFeedback = round(goRTFeedback, 2)
    else:
        goRTFeedback = 'Null'
    
    if goTrialCount > 0:
        commissionRate = (commissionCount/goTrialCount)
        commissionRate = round(commissionRate, 2)
        omissionRate = (omissionCount/goTrialCount)
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
    
    testBlockCount += 1
    block +=1
    stopMessage = f"You have completed {testBlockCount} of {numTestBlocks}."
    
    if testBlockCount == numTestBlocks:
        stopMessage += "\n You have finished the testing phase."
    else:
        stopMessage += "\nPlease take this time to read your feedback if there is any, and take a 1 minute break.\n"
        
        if commissionRate > commision_thresh:
            stopMessage += "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Index Finger" \
                            + "\n\tSquare: Middle Finger"
                            
        if goRTFeedback != 'Null' and goRTFeedback > rt_thresh:
            stopMessage += "\nYou have been responding too slowly, please respond to each shape as quickly and as accurately as possible."
    
        if omissionRate > missed_response_thresh:
            if commissionRate > commision_thresh:
                stopMessage += "\n\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes."
            else:
                stopMessage += "\n\nWe have detected a number of trials that required a response, where no response was made.  Please ensure that you are responding accurately and quickly to the shapes." \
                            + "\n Your accuracy is too low. Remember:" \
                            + "\n\tCircle: Index Finger" \
                            + "\n\tSquare: Middle Finger"
    
        if probabilityOfStop < minStopCorrect:
            stopMessage += "\nYou have not been stopping your response when stars are present.  Please try your best to stop your response if you see a star."
        elif probabilityOfStop > maxStopCorrect:
            stopMessage += "\nDo not slow down and wait for the star to appear. Please respond as quickly and accurately as possible when a star does not appear."
            
    stopMessage += "\n\nPress enter to continue."
    
    
    print(f'comission_rate: {commissionRate}, omission_rate: {omissionRate}')
    print(stopMessage)
    
    #***************************
    
    stopTrialList = createTrialTypes(numTrialsPerBlock, color, shapes, conditions, totalShapesUsed)
    
    thisExp.addData(f"Test Block: {testBlockCount}", stopTrialList)
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
    while continueRoutine and routineTimer.getTime() < 60.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_6* updates
        if text_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_6.frameNStart = frameN  # exact frame index
            text_6.tStart = t  # local t and not account for scr refresh
            text_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_6.started')
            text_6.setAutoDraw(True)
        if text_6.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_6.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                text_6.tStop = t  # not accounting for scr refresh
                text_6.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_6.stopped')
                text_6.setAutoDraw(False)
        
        # *key_resp_4* updates
        waitOnFlip = False
        if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_4.frameNStart = frameN  # exact frame index
            key_resp_4.tStart = t  # local t and not account for scr refresh
            key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_4.started')
            key_resp_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_4.tStop = t  # not accounting for scr refresh
                key_resp_4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_4.stopped')
                key_resp_4.status = FINISHED
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
    if key_resp_4.keys is not None:  # we had a response
        stopBlocks.addData('key_resp_4.rt', key_resp_4.rt)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-60.000000)
    thisExp.nextEntry()
    
# completed numTestBlocks repeats of 'stopBlocks'


# --- Prepare to start Routine "end" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
end_resp.keys = []
end_resp.rt = []
_end_resp_allKeys = []
# keep track of which components have finished
endComponents = [ending_text, end_resp]
for thisComponent in endComponents:
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

# --- Run Routine "end" ---
while continueRoutine and routineTimer.getTime() < 300.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ending_text* updates
    if ending_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ending_text.frameNStart = frameN  # exact frame index
        ending_text.tStart = t  # local t and not account for scr refresh
        ending_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ending_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ending_text.started')
        ending_text.setAutoDraw(True)
    if ending_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ending_text.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            ending_text.tStop = t  # not accounting for scr refresh
            ending_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ending_text.stopped')
            ending_text.setAutoDraw(False)
    
    # *end_resp* updates
    waitOnFlip = False
    if end_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_resp.frameNStart = frameN  # exact frame index
        end_resp.tStart = t  # local t and not account for scr refresh
        end_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'end_resp.started')
        end_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(end_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(end_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if end_resp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_resp.tStartRefresh + 300-frameTolerance:
            # keep track of stop time/frame for later
            end_resp.tStop = t  # not accounting for scr refresh
            end_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_resp.stopped')
            end_resp.status = FINISHED
    if end_resp.status == STARTED and not waitOnFlip:
        theseKeys = end_resp.getKeys(keyList=['return'], waitRelease=False)
        _end_resp_allKeys.extend(theseKeys)
        if len(_end_resp_allKeys):
            end_resp.keys = _end_resp_allKeys[-1].name  # just the last key pressed
            end_resp.rt = _end_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "end" ---
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if end_resp.keys in ['', [], None]:  # No response was made
    end_resp.keys = None
thisExp.addData('end_resp.keys',end_resp.keys)
if end_resp.keys is not None:  # we had a response
    thisExp.addData('end_resp.rt', end_resp.rt)
thisExp.nextEntry()
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-300.000000)

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
