#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Tue Mar 11 13:26:31 2025
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
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

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
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'simplestop_skeleton'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [2560, 1440]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/kritiaxh/Documents/paperRepos/SharedControlPaper/experiments/simpleStop/simpleStop_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('start_exp') is None:
        # initialise start_exp
        start_exp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='start_exp',
        )
    if deviceManager.getDevice('start_prac') is None:
        # initialise start_prac
        start_prac = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='start_prac',
        )
    if deviceManager.getDevice('goResp') is None:
        # initialise goResp
        goResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='goResp',
        )
    if deviceManager.getDevice('key_resp_3') is None:
        # initialise key_resp_3
        key_resp_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_3',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('goResp_test') is None:
        # initialise goResp_test
        goResp_test = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='goResp_test',
        )
    if deviceManager.getDevice('key_resp_4') is None:
        # initialise key_resp_4
        key_resp_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_4',
        )
    if deviceManager.getDevice('end_resp') is None:
        # initialise end_resp
        end_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='end_resp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "start" ---
    welcome = visual.TextStim(win=win, name='welcome',
        text='Welcome to the task!\n\nPress enter to continue.',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.045, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    start_exp = keyboard.Keyboard(deviceName='start_exp')
    
    # --- Initialize components for Routine "StimSetup" ---
    # Run 'Begin Experiment' code from stim_setup
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
        pos=[0, 0], draggable=False, height=0.025, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    start_prac = keyboard.Keyboard(deviceName='start_prac')
    
    # --- Initialize components for Routine "practiceBlockSetup" ---
    # Run 'Begin Experiment' code from practice_block
    block = 1
    
    
    # --- Initialize components for Routine "newPracticeStim" ---
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextStim(win=win, name='fixation',
        text='+',
        font='Arial',
        pos=[0, 0], draggable=False, height=.15, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    goStim = visual.ImageStim(
        win=win,
        name='goStim', units='pix', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=[0,0], draggable=False, size=[151, 151],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    goResp = keyboard.Keyboard(deviceName='goResp')
    stopSignal = visual.ImageStim(
        win=win,
        name='stopSignal', 
        image='stopSignal.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    rules = visual.TextStim(win=win, name='rules',
        text='Circle: Index Finger\nSquare: Middle Finger\nDo not respond if a star appears!',
        font='Open Sans',
        pos=(-.6, .4), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    
    # --- Initialize components for Routine "feedback" ---
    # Run 'Begin Experiment' code from practice_feedback
    #***************************
    
    #message variable just needs some value at start
    feedbackMessage=None
    
    #***************************
    text = visual.TextStim(win=win, name='text',
        text='',
        font='Arial',
        pos=[0, 0], draggable=False, height=0.05, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    rules_2 = visual.TextStim(win=win, name='rules_2',
        text='Circle: Index Finger\nSquare: Middle Finger\nDo not respond if a star appears!',
        font='Open Sans',
        pos=(-.6, .4), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "endTrial" ---
    
    # --- Initialize components for Routine "practiceFeedback" ---
    text_5 = visual.TextStim(win=win, name='text_5',
        text='',
        font='Arial',
        pos=[0, 0], draggable=False, height=0.025, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_3 = keyboard.Keyboard(deviceName='key_resp_3')
    
    # --- Initialize components for Routine "practiceRepeat" ---
    
    # --- Initialize components for Routine "testInstructions" ---
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    testText = visual.TextStim(win=win, name='testText',
        text='We will now begin the testing phase. To summarize the instructions.\n\nIf the shape is a circle press Index Finger.\nIf the shape is a square press Middle Finger.\n\nYou should respond as quickly and accurately as possible to each shape.\n \nOn some trials, a star will appear around the shape. If you see a star appear, please try your best to withhold your response on that trial.\n\nPlease do not slow down your responses to wait for the star to appear.  You should respond as quickly and accurately as possible as soon as you see the shapes appear on the screen.\n\nPress enter to start the testing.\n\n',
        font='Arial',
        pos=[0, 0], draggable=False, height=0.025, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    # Run 'Begin Experiment' code from test_setup
    testBlockCount = 0
    stopTrialList = createTrialTypes(numTrialsPerBlock, color, shapes, conditions, totalShapesUsed)
    
    thisExp.addData(f"Test Block: 1", stopTrialList)
    
    # --- Initialize components for Routine "stopBlockSetup" ---
    
    # --- Initialize components for Routine "newStopStim" ---
    
    # --- Initialize components for Routine "test_trial" ---
    test_fixation = visual.TextStim(win=win, name='test_fixation',
        text='+',
        font='Arial',
        pos=[0, 0], draggable=False, height=.15, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    goStim_test = visual.ImageStim(
        win=win,
        name='goStim_test', units='pix', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=[0,0], draggable=False, size=[151, 151],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    goResp_test = keyboard.Keyboard(deviceName='goResp_test')
    stopSignal_test = visual.ImageStim(
        win=win,
        name='stopSignal_test', 
        image='stopSignal.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    
    # --- Initialize components for Routine "ssdChange" ---
    
    # --- Initialize components for Routine "endOfStopBlockFeedback" ---
    text_6 = visual.TextStim(win=win, name='text_6',
        text='',
        font='Arial',
        pos=[0, 0], draggable=False, height=0.025, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_4 = keyboard.Keyboard(deviceName='key_resp_4')
    
    # --- Initialize components for Routine "end" ---
    ending_text = visual.TextStim(win=win, name='ending_text',
        text='Thanks for completing this task!\nPress enter to end.',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    end_resp = keyboard.Keyboard(deviceName='end_resp')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "start" ---
    # create an object to store info about Routine start
    start = data.Routine(
        name='start',
        components=[welcome, start_exp],
    )
    start.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for start_exp
    start_exp.keys = []
    start_exp.rt = []
    _start_exp_allKeys = []
    # store start times for start
    start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    start.tStart = globalClock.getTime(format='float')
    start.status = STARTED
    thisExp.addData('start.started', start.tStart)
    start.maxDuration = None
    # keep track of which components have finished
    startComponents = start.components
    for thisComponent in start.components:
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
    start.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 300.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *welcome* updates
        
        # if welcome is starting this frame...
        if welcome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            welcome.frameNStart = frameN  # exact frame index
            welcome.tStart = t  # local t and not account for scr refresh
            welcome.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcome, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcome.started')
            # update status
            welcome.status = STARTED
            welcome.setAutoDraw(True)
        
        # if welcome is active this frame...
        if welcome.status == STARTED:
            # update params
            pass
        
        # if welcome is stopping this frame...
        if welcome.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > welcome.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                welcome.tStop = t  # not accounting for scr refresh
                welcome.tStopRefresh = tThisFlipGlobal  # on global time
                welcome.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'welcome.stopped')
                # update status
                welcome.status = FINISHED
                welcome.setAutoDraw(False)
        
        # *start_exp* updates
        waitOnFlip = False
        
        # if start_exp is starting this frame...
        if start_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_exp.frameNStart = frameN  # exact frame index
            start_exp.tStart = t  # local t and not account for scr refresh
            start_exp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_exp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_exp.started')
            # update status
            start_exp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(start_exp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(start_exp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if start_exp is stopping this frame...
        if start_exp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > start_exp.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                start_exp.tStop = t  # not accounting for scr refresh
                start_exp.tStopRefresh = tThisFlipGlobal  # on global time
                start_exp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'start_exp.stopped')
                # update status
                start_exp.status = FINISHED
                start_exp.status = FINISHED
        if start_exp.status == STARTED and not waitOnFlip:
            theseKeys = start_exp.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
            _start_exp_allKeys.extend(theseKeys)
            if len(_start_exp_allKeys):
                start_exp.keys = _start_exp_allKeys[-1].name  # just the last key pressed
                start_exp.rt = _start_exp_allKeys[-1].rt
                start_exp.duration = _start_exp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            start.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "start" ---
    for thisComponent in start.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for start
    start.tStop = globalClock.getTime(format='float')
    start.tStopRefresh = tThisFlipGlobal
    thisExp.addData('start.stopped', start.tStop)
    # check responses
    if start_exp.keys in ['', [], None]:  # No response was made
        start_exp.keys = None
    thisExp.addData('start_exp.keys',start_exp.keys)
    if start_exp.keys != None:  # we had a response
        thisExp.addData('start_exp.rt', start_exp.rt)
        thisExp.addData('start_exp.duration', start_exp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if start.maxDurationReached:
        routineTimer.addTime(-start.maxDuration)
    elif start.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-300.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "StimSetup" ---
    # create an object to store info about Routine StimSetup
    StimSetup = data.Routine(
        name='StimSetup',
        components=[],
    )
    StimSetup.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for StimSetup
    StimSetup.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    StimSetup.tStart = globalClock.getTime(format='float')
    StimSetup.status = STARTED
    thisExp.addData('StimSetup.started', StimSetup.tStart)
    StimSetup.maxDuration = None
    # keep track of which components have finished
    StimSetupComponents = StimSetup.components
    for thisComponent in StimSetup.components:
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
    StimSetup.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            StimSetup.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in StimSetup.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "StimSetup" ---
    for thisComponent in StimSetup.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for StimSetup
    StimSetup.tStop = globalClock.getTime(format='float')
    StimSetup.tStopRefresh = tThisFlipGlobal
    thisExp.addData('StimSetup.stopped', StimSetup.tStop)
    thisExp.nextEntry()
    # the Routine "StimSetup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instrStopText, start_prac],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for start_prac
    start_prac.keys = []
    start_prac.rt = []
    _start_prac_allKeys = []
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
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
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 180.0:
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
        
        # if instrStopText is stopping this frame...
        if instrStopText.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > instrStopText.tStartRefresh + 180-frameTolerance:
                # keep track of stop time/frame for later
                instrStopText.tStop = t  # not accounting for scr refresh
                instrStopText.tStopRefresh = tThisFlipGlobal  # on global time
                instrStopText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instrStopText.stopped')
                # update status
                instrStopText.status = FINISHED
                instrStopText.setAutoDraw(False)
        
        # *start_prac* updates
        waitOnFlip = False
        
        # if start_prac is starting this frame...
        if start_prac.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_prac.frameNStart = frameN  # exact frame index
            start_prac.tStart = t  # local t and not account for scr refresh
            start_prac.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_prac, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_prac.started')
            # update status
            start_prac.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(start_prac.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(start_prac.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if start_prac is stopping this frame...
        if start_prac.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > start_prac.tStartRefresh + 180-frameTolerance:
                # keep track of stop time/frame for later
                start_prac.tStop = t  # not accounting for scr refresh
                start_prac.tStopRefresh = tThisFlipGlobal  # on global time
                start_prac.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'start_prac.stopped')
                # update status
                start_prac.status = FINISHED
                start_prac.status = FINISHED
        if start_prac.status == STARTED and not waitOnFlip:
            theseKeys = start_prac.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
            _start_prac_allKeys.extend(theseKeys)
            if len(_start_prac_allKeys):
                start_prac.keys = _start_prac_allKeys[-1].name  # just the last key pressed
                start_prac.rt = _start_prac_allKeys[-1].rt
                start_prac.duration = _start_prac_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if instructions.maxDurationReached:
        routineTimer.addTime(-instructions.maxDuration)
    elif instructions.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-180.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    practiceBlocks = data.TrialHandler2(
        name='practiceBlocks',
        nReps=3.0, 
        method='fullRandom', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(practiceBlocks)  # add the loop to the experiment
    thisPracticeBlock = practiceBlocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
    if thisPracticeBlock != None:
        for paramName in thisPracticeBlock:
            globals()[paramName] = thisPracticeBlock[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPracticeBlock in practiceBlocks:
        currentLoop = practiceBlocks
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPracticeBlock.rgb)
        if thisPracticeBlock != None:
            for paramName in thisPracticeBlock:
                globals()[paramName] = thisPracticeBlock[paramName]
        
        # --- Prepare to start Routine "practiceBlockSetup" ---
        # create an object to store info about Routine practiceBlockSetup
        practiceBlockSetup = data.Routine(
            name='practiceBlockSetup',
            components=[],
        )
        practiceBlockSetup.status = NOT_STARTED
        continueRoutine = True
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
        # store start times for practiceBlockSetup
        practiceBlockSetup.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practiceBlockSetup.tStart = globalClock.getTime(format='float')
        practiceBlockSetup.status = STARTED
        thisExp.addData('practiceBlockSetup.started', practiceBlockSetup.tStart)
        practiceBlockSetup.maxDuration = None
        # keep track of which components have finished
        practiceBlockSetupComponents = practiceBlockSetup.components
        for thisComponent in practiceBlockSetup.components:
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
        # if trial has changed, end Routine now
        if isinstance(practiceBlocks, data.TrialHandler2) and thisPracticeBlock.thisN != practiceBlocks.thisTrial.thisN:
            continueRoutine = False
        practiceBlockSetup.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                practiceBlockSetup.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in practiceBlockSetup.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practiceBlockSetup" ---
        for thisComponent in practiceBlockSetup.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practiceBlockSetup
        practiceBlockSetup.tStop = globalClock.getTime(format='float')
        practiceBlockSetup.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practiceBlockSetup.stopped', practiceBlockSetup.tStop)
        # the Routine "practiceBlockSetup" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        practiceTrials = data.TrialHandler2(
            name='practiceTrials',
            nReps=6.0, 
            method='fullRandom', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions('condition.xlsx'), 
            seed=None, 
        )
        thisExp.addLoop(practiceTrials)  # add the loop to the experiment
        thisPracticeTrial = practiceTrials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
        if thisPracticeTrial != None:
            for paramName in thisPracticeTrial:
                globals()[paramName] = thisPracticeTrial[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisPracticeTrial in practiceTrials:
            currentLoop = practiceTrials
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
            if thisPracticeTrial != None:
                for paramName in thisPracticeTrial:
                    globals()[paramName] = thisPracticeTrial[paramName]
            
            # --- Prepare to start Routine "newPracticeStim" ---
            # create an object to store info about Routine newPracticeStim
            newPracticeStim = data.Routine(
                name='newPracticeStim',
                components=[],
            )
            newPracticeStim.status = NOT_STARTED
            continueRoutine = True
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
            # store start times for newPracticeStim
            newPracticeStim.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            newPracticeStim.tStart = globalClock.getTime(format='float')
            newPracticeStim.status = STARTED
            thisExp.addData('newPracticeStim.started', newPracticeStim.tStart)
            newPracticeStim.maxDuration = None
            # keep track of which components have finished
            newPracticeStimComponents = newPracticeStim.components
            for thisComponent in newPracticeStim.components:
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
            # if trial has changed, end Routine now
            if isinstance(practiceTrials, data.TrialHandler2) and thisPracticeTrial.thisN != practiceTrials.thisTrial.thisN:
                continueRoutine = False
            newPracticeStim.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    newPracticeStim.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in newPracticeStim.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "newPracticeStim" ---
            for thisComponent in newPracticeStim.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for newPracticeStim
            newPracticeStim.tStop = globalClock.getTime(format='float')
            newPracticeStim.tStopRefresh = tThisFlipGlobal
            thisExp.addData('newPracticeStim.stopped', newPracticeStim.tStop)
            # the Routine "newPracticeStim" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "trial" ---
            # create an object to store info about Routine trial
            trial = data.Routine(
                name='trial',
                components=[fixation, goStim, goResp, stopSignal, rules],
            )
            trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            goStim.setPos([0, 0])
            goStim.setImage(currentGoStim)
            # create starting attributes for goResp
            goResp.keys = []
            goResp.rt = []
            _goResp_allKeys = []
            # store start times for trial
            trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            trial.tStart = globalClock.getTime(format='float')
            trial.status = STARTED
            thisExp.addData('trial.started', trial.tStart)
            trial.maxDuration = None
            # keep track of which components have finished
            trialComponents = trial.components
            for thisComponent in trial.components:
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
            # if trial has changed, end Routine now
            if isinstance(practiceTrials, data.TrialHandler2) and thisPracticeTrial.thisN != practiceTrials.thisTrial.thisN:
                continueRoutine = False
            trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
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
                        fixation.tStopRefresh = tThisFlipGlobal  # on global time
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
                    if tThisFlipGlobal > goStim.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        goStim.tStop = t  # not accounting for scr refresh
                        goStim.tStopRefresh = tThisFlipGlobal  # on global time
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
                    if tThisFlipGlobal > goResp.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        goResp.tStop = t  # not accounting for scr refresh
                        goResp.tStopRefresh = tThisFlipGlobal  # on global time
                        goResp.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'goResp.stopped')
                        # update status
                        goResp.status = FINISHED
                        goResp.status = FINISHED
                if goResp.status == STARTED and not waitOnFlip:
                    theseKeys = goResp.getKeys(keyList=['left', 'right'], ignoreKeys=["escape"], waitRelease=False)
                    _goResp_allKeys.extend(theseKeys)
                    if len(_goResp_allKeys):
                        goResp.keys = _goResp_allKeys[0].name  # just the first key pressed
                        goResp.rt = _goResp_allKeys[0].rt
                        goResp.duration = _goResp_allKeys[0].duration
                        # was this correct?
                        if (goResp.keys == str(currentCorrectResponse)) or (goResp.keys == currentCorrectResponse):
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
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > stopSignal.tStartRefresh + .5-frameTolerance:
                        # keep track of stop time/frame for later
                        stopSignal.tStop = t  # not accounting for scr refresh
                        stopSignal.tStopRefresh = tThisFlipGlobal  # on global time
                        stopSignal.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'stopSignal.stopped')
                        # update status
                        stopSignal.status = FINISHED
                        stopSignal.setAutoDraw(False)
                
                # *rules* updates
                
                # if rules is starting this frame...
                if rules.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    rules.frameNStart = frameN  # exact frame index
                    rules.tStart = t  # local t and not account for scr refresh
                    rules.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(rules, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rules.started')
                    # update status
                    rules.status = STARTED
                    rules.setAutoDraw(True)
                
                # if rules is active this frame...
                if rules.status == STARTED:
                    # update params
                    pass
                
                # if rules is stopping this frame...
                if rules.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > rules.tStartRefresh + 2.5-frameTolerance:
                        # keep track of stop time/frame for later
                        rules.tStop = t  # not accounting for scr refresh
                        rules.tStopRefresh = tThisFlipGlobal  # on global time
                        rules.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'rules.stopped')
                        # update status
                        rules.status = FINISHED
                        rules.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    trial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "trial" ---
            for thisComponent in trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for trial
            trial.tStop = globalClock.getTime(format='float')
            trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('trial.stopped', trial.tStop)
            # check responses
            if goResp.keys in ['', [], None]:  # No response was made
                goResp.keys = None
                # was no response the correct answer?!
                if str(currentCorrectResponse).lower() == 'none':
                   goResp.corr = 1;  # correct non-response
                else:
                   goResp.corr = 0;  # failed to respond (incorrectly)
            # store data for practiceTrials (TrialHandler)
            practiceTrials.addData('goResp.keys',goResp.keys)
            practiceTrials.addData('goResp.corr', goResp.corr)
            if goResp.keys != None:  # we had a response
                practiceTrials.addData('goResp.rt', goResp.rt)
                practiceTrials.addData('goResp.duration', goResp.duration)
            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "feedback" ---
            # create an object to store info about Routine feedback
            feedback = data.Routine(
                name='feedback',
                components=[text, rules_2],
            )
            feedback.status = NOT_STARTED
            continueRoutine = True
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
            # store start times for feedback
            feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            feedback.tStart = globalClock.getTime(format='float')
            feedback.status = STARTED
            thisExp.addData('feedback.started', feedback.tStart)
            feedback.maxDuration = None
            # keep track of which components have finished
            feedbackComponents = feedback.components
            for thisComponent in feedback.components:
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
            # if trial has changed, end Routine now
            if isinstance(practiceTrials, data.TrialHandler2) and thisPracticeTrial.thisN != practiceTrials.thisTrial.thisN:
                continueRoutine = False
            feedback.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 0.5:
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
                    if tThisFlipGlobal > text.tStartRefresh + .5-frameTolerance:
                        # keep track of stop time/frame for later
                        text.tStop = t  # not accounting for scr refresh
                        text.tStopRefresh = tThisFlipGlobal  # on global time
                        text.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text.stopped')
                        # update status
                        text.status = FINISHED
                        text.setAutoDraw(False)
                
                # *rules_2* updates
                
                # if rules_2 is starting this frame...
                if rules_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    rules_2.frameNStart = frameN  # exact frame index
                    rules_2.tStart = t  # local t and not account for scr refresh
                    rules_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(rules_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rules_2.started')
                    # update status
                    rules_2.status = STARTED
                    rules_2.setAutoDraw(True)
                
                # if rules_2 is active this frame...
                if rules_2.status == STARTED:
                    # update params
                    pass
                
                # if rules_2 is stopping this frame...
                if rules_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > rules_2.tStartRefresh + .5-frameTolerance:
                        # keep track of stop time/frame for later
                        rules_2.tStop = t  # not accounting for scr refresh
                        rules_2.tStopRefresh = tThisFlipGlobal  # on global time
                        rules_2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'rules_2.stopped')
                        # update status
                        rules_2.status = FINISHED
                        rules_2.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    feedback.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in feedback.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "feedback" ---
            for thisComponent in feedback.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for feedback
            feedback.tStop = globalClock.getTime(format='float')
            feedback.tStopRefresh = tThisFlipGlobal
            thisExp.addData('feedback.stopped', feedback.tStop)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if feedback.maxDurationReached:
                routineTimer.addTime(-feedback.maxDuration)
            elif feedback.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-0.500000)
            
            # --- Prepare to start Routine "endTrial" ---
            # create an object to store info about Routine endTrial
            endTrial = data.Routine(
                name='endTrial',
                components=[],
            )
            endTrial.status = NOT_STARTED
            continueRoutine = True
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
            # store start times for endTrial
            endTrial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            endTrial.tStart = globalClock.getTime(format='float')
            endTrial.status = STARTED
            thisExp.addData('endTrial.started', endTrial.tStart)
            endTrial.maxDuration = None
            # keep track of which components have finished
            endTrialComponents = endTrial.components
            for thisComponent in endTrial.components:
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
            # if trial has changed, end Routine now
            if isinstance(practiceTrials, data.TrialHandler2) and thisPracticeTrial.thisN != practiceTrials.thisTrial.thisN:
                continueRoutine = False
            endTrial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    endTrial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in endTrial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "endTrial" ---
            for thisComponent in endTrial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for endTrial
            endTrial.tStop = globalClock.getTime(format='float')
            endTrial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('endTrial.stopped', endTrial.tStop)
            # Run 'End Routine' code from practice_trial_end
            practiceTrials.addData("EndTrialTimeStamp", core.getTime())
            practiceTrials.addData("Phase", phase)
            practiceTrials.addData("Block", block)
            # the Routine "endTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 6.0 repeats of 'practiceTrials'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "practiceFeedback" ---
        # create an object to store info about Routine practiceFeedback
        practiceFeedback = data.Routine(
            name='practiceFeedback',
            components=[text_5, key_resp_3],
        )
        practiceFeedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from practice_block_feedback
        #***************************
        import numpy as np
        
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
        # create starting attributes for key_resp_3
        key_resp_3.keys = []
        key_resp_3.rt = []
        _key_resp_3_allKeys = []
        # store start times for practiceFeedback
        practiceFeedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practiceFeedback.tStart = globalClock.getTime(format='float')
        practiceFeedback.status = STARTED
        thisExp.addData('practiceFeedback.started', practiceFeedback.tStart)
        practiceFeedback.maxDuration = None
        # keep track of which components have finished
        practiceFeedbackComponents = practiceFeedback.components
        for thisComponent in practiceFeedback.components:
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
        # if trial has changed, end Routine now
        if isinstance(practiceBlocks, data.TrialHandler2) and thisPracticeBlock.thisN != practiceBlocks.thisTrial.thisN:
            continueRoutine = False
        practiceFeedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 60.0:
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
            
            # if text_5 is stopping this frame...
            if text_5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_5.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    text_5.tStop = t  # not accounting for scr refresh
                    text_5.tStopRefresh = tThisFlipGlobal  # on global time
                    text_5.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_5.stopped')
                    # update status
                    text_5.status = FINISHED
                    text_5.setAutoDraw(False)
            
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
            
            # if key_resp_3 is stopping this frame...
            if key_resp_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_3.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_3.tStop = t  # not accounting for scr refresh
                    key_resp_3.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp_3.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_3.stopped')
                    # update status
                    key_resp_3.status = FINISHED
                    key_resp_3.status = FINISHED
            if key_resp_3.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_3.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_3_allKeys.extend(theseKeys)
                if len(_key_resp_3_allKeys):
                    key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                    key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                    key_resp_3.duration = _key_resp_3_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                practiceFeedback.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in practiceFeedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practiceFeedback" ---
        for thisComponent in practiceFeedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practiceFeedback
        practiceFeedback.tStop = globalClock.getTime(format='float')
        practiceFeedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practiceFeedback.stopped', practiceFeedback.tStop)
        # check responses
        if key_resp_3.keys in ['', [], None]:  # No response was made
            key_resp_3.keys = None
        practiceBlocks.addData('key_resp_3.keys',key_resp_3.keys)
        if key_resp_3.keys != None:  # we had a response
            practiceBlocks.addData('key_resp_3.rt', key_resp_3.rt)
            practiceBlocks.addData('key_resp_3.duration', key_resp_3.duration)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if practiceFeedback.maxDurationReached:
            routineTimer.addTime(-practiceFeedback.maxDuration)
        elif practiceFeedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-60.000000)
        
        # --- Prepare to start Routine "practiceRepeat" ---
        # create an object to store info about Routine practiceRepeat
        practiceRepeat = data.Routine(
            name='practiceRepeat',
            components=[],
        )
        practiceRepeat.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from practice_block_loop
        stopPracTrialList = createTrialTypes(numStopPracTrials, color, shapes, conditions, totalShapesUsed)
        
        thisExp.addData("stopPracTrialList", stopPracTrialList)
        if practiceEnd == 1:
            practiceBlocks.finished = True
        # store start times for practiceRepeat
        practiceRepeat.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practiceRepeat.tStart = globalClock.getTime(format='float')
        practiceRepeat.status = STARTED
        thisExp.addData('practiceRepeat.started', practiceRepeat.tStart)
        practiceRepeat.maxDuration = None
        # keep track of which components have finished
        practiceRepeatComponents = practiceRepeat.components
        for thisComponent in practiceRepeat.components:
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
        # if trial has changed, end Routine now
        if isinstance(practiceBlocks, data.TrialHandler2) and thisPracticeBlock.thisN != practiceBlocks.thisTrial.thisN:
            continueRoutine = False
        practiceRepeat.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                practiceRepeat.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in practiceRepeat.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practiceRepeat" ---
        for thisComponent in practiceRepeat.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practiceRepeat
        practiceRepeat.tStop = globalClock.getTime(format='float')
        practiceRepeat.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practiceRepeat.stopped', practiceRepeat.tStop)
        # the Routine "practiceRepeat" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 3.0 repeats of 'practiceBlocks'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "testInstructions" ---
    # create an object to store info about Routine testInstructions
    testInstructions = data.Routine(
        name='testInstructions',
        components=[key_resp, testText],
    )
    testInstructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # Run 'Begin Routine' code from test_setup
    phase = "test"
    block = 1
    # store start times for testInstructions
    testInstructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    testInstructions.tStart = globalClock.getTime(format='float')
    testInstructions.status = STARTED
    thisExp.addData('testInstructions.started', testInstructions.tStart)
    testInstructions.maxDuration = None
    # keep track of which components have finished
    testInstructionsComponents = testInstructions.components
    for thisComponent in testInstructions.components:
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
    testInstructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 300.0:
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
        
        # if key_resp is stopping this frame...
        if key_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                key_resp.tStop = t  # not accounting for scr refresh
                key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                key_resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.stopped')
                # update status
                key_resp.status = FINISHED
                key_resp.status = FINISHED
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
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
        
        # if testText is stopping this frame...
        if testText.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > testText.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                testText.tStop = t  # not accounting for scr refresh
                testText.tStopRefresh = tThisFlipGlobal  # on global time
                testText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'testText.stopped')
                # update status
                testText.status = FINISHED
                testText.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            testInstructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testInstructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "testInstructions" ---
    for thisComponent in testInstructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for testInstructions
    testInstructions.tStop = globalClock.getTime(format='float')
    testInstructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('testInstructions.stopped', testInstructions.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if testInstructions.maxDurationReached:
        routineTimer.addTime(-testInstructions.maxDuration)
    elif testInstructions.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-300.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    stopBlocks = data.TrialHandler2(
        name='stopBlocks',
        nReps=numTestBlocks, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(stopBlocks)  # add the loop to the experiment
    thisStopBlock = stopBlocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
    if thisStopBlock != None:
        for paramName in thisStopBlock:
            globals()[paramName] = thisStopBlock[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisStopBlock in stopBlocks:
        currentLoop = stopBlocks
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
        if thisStopBlock != None:
            for paramName in thisStopBlock:
                globals()[paramName] = thisStopBlock[paramName]
        
        # --- Prepare to start Routine "stopBlockSetup" ---
        # create an object to store info about Routine stopBlockSetup
        stopBlockSetup = data.Routine(
            name='stopBlockSetup',
            components=[],
        )
        stopBlockSetup.status = NOT_STARTED
        continueRoutine = True
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
        
        
        # store start times for stopBlockSetup
        stopBlockSetup.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        stopBlockSetup.tStart = globalClock.getTime(format='float')
        stopBlockSetup.status = STARTED
        thisExp.addData('stopBlockSetup.started', stopBlockSetup.tStart)
        stopBlockSetup.maxDuration = None
        # keep track of which components have finished
        stopBlockSetupComponents = stopBlockSetup.components
        for thisComponent in stopBlockSetup.components:
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
        # if trial has changed, end Routine now
        if isinstance(stopBlocks, data.TrialHandler2) and thisStopBlock.thisN != stopBlocks.thisTrial.thisN:
            continueRoutine = False
        stopBlockSetup.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                stopBlockSetup.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in stopBlockSetup.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "stopBlockSetup" ---
        for thisComponent in stopBlockSetup.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for stopBlockSetup
        stopBlockSetup.tStop = globalClock.getTime(format='float')
        stopBlockSetup.tStopRefresh = tThisFlipGlobal
        thisExp.addData('stopBlockSetup.stopped', stopBlockSetup.tStop)
        # the Routine "stopBlockSetup" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        testTrials = data.TrialHandler2(
            name='testTrials',
            nReps=12.0, 
            method='fullRandom', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions('condition.xlsx'), 
            seed=None, 
        )
        thisExp.addLoop(testTrials)  # add the loop to the experiment
        thisTestTrial = testTrials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
        if thisTestTrial != None:
            for paramName in thisTestTrial:
                globals()[paramName] = thisTestTrial[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTestTrial in testTrials:
            currentLoop = testTrials
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTestTrial.rgb)
            if thisTestTrial != None:
                for paramName in thisTestTrial:
                    globals()[paramName] = thisTestTrial[paramName]
            
            # --- Prepare to start Routine "newStopStim" ---
            # create an object to store info about Routine newStopStim
            newStopStim = data.Routine(
                name='newStopStim',
                components=[],
            )
            newStopStim.status = NOT_STARTED
            continueRoutine = True
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
            # store start times for newStopStim
            newStopStim.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            newStopStim.tStart = globalClock.getTime(format='float')
            newStopStim.status = STARTED
            thisExp.addData('newStopStim.started', newStopStim.tStart)
            newStopStim.maxDuration = None
            # keep track of which components have finished
            newStopStimComponents = newStopStim.components
            for thisComponent in newStopStim.components:
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
            # if trial has changed, end Routine now
            if isinstance(testTrials, data.TrialHandler2) and thisTestTrial.thisN != testTrials.thisTrial.thisN:
                continueRoutine = False
            newStopStim.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    newStopStim.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in newStopStim.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "newStopStim" ---
            for thisComponent in newStopStim.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for newStopStim
            newStopStim.tStop = globalClock.getTime(format='float')
            newStopStim.tStopRefresh = tThisFlipGlobal
            thisExp.addData('newStopStim.stopped', newStopStim.tStop)
            # the Routine "newStopStim" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "test_trial" ---
            # create an object to store info about Routine test_trial
            test_trial = data.Routine(
                name='test_trial',
                components=[test_fixation, goStim_test, goResp_test, stopSignal_test],
            )
            test_trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            goStim_test.setPos([0, 0])
            goStim_test.setImage(currentGoStim)
            # create starting attributes for goResp_test
            goResp_test.keys = []
            goResp_test.rt = []
            _goResp_test_allKeys = []
            # store start times for test_trial
            test_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            test_trial.tStart = globalClock.getTime(format='float')
            test_trial.status = STARTED
            thisExp.addData('test_trial.started', test_trial.tStart)
            test_trial.maxDuration = None
            # keep track of which components have finished
            test_trialComponents = test_trial.components
            for thisComponent in test_trial.components:
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
            # if trial has changed, end Routine now
            if isinstance(testTrials, data.TrialHandler2) and thisTestTrial.thisN != testTrials.thisTrial.thisN:
                continueRoutine = False
            test_trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *test_fixation* updates
                
                # if test_fixation is starting this frame...
                if test_fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    test_fixation.frameNStart = frameN  # exact frame index
                    test_fixation.tStart = t  # local t and not account for scr refresh
                    test_fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(test_fixation, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'test_fixation.started')
                    # update status
                    test_fixation.status = STARTED
                    test_fixation.setAutoDraw(True)
                
                # if test_fixation is active this frame...
                if test_fixation.status == STARTED:
                    # update params
                    pass
                
                # if test_fixation is stopping this frame...
                if test_fixation.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > test_fixation.tStartRefresh + .5-frameTolerance:
                        # keep track of stop time/frame for later
                        test_fixation.tStop = t  # not accounting for scr refresh
                        test_fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        test_fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'test_fixation.stopped')
                        # update status
                        test_fixation.status = FINISHED
                        test_fixation.setAutoDraw(False)
                
                # *goStim_test* updates
                
                # if goStim_test is starting this frame...
                if goStim_test.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                    # keep track of start time/frame for later
                    goStim_test.frameNStart = frameN  # exact frame index
                    goStim_test.tStart = t  # local t and not account for scr refresh
                    goStim_test.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(goStim_test, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goStim_test.started')
                    # update status
                    goStim_test.status = STARTED
                    goStim_test.setAutoDraw(True)
                
                # if goStim_test is active this frame...
                if goStim_test.status == STARTED:
                    # update params
                    pass
                
                # if goStim_test is stopping this frame...
                if goStim_test.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > goStim_test.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        goStim_test.tStop = t  # not accounting for scr refresh
                        goStim_test.tStopRefresh = tThisFlipGlobal  # on global time
                        goStim_test.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'goStim_test.stopped')
                        # update status
                        goStim_test.status = FINISHED
                        goStim_test.setAutoDraw(False)
                
                # *goResp_test* updates
                waitOnFlip = False
                
                # if goResp_test is starting this frame...
                if goResp_test.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                    # keep track of start time/frame for later
                    goResp_test.frameNStart = frameN  # exact frame index
                    goResp_test.tStart = t  # local t and not account for scr refresh
                    goResp_test.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(goResp_test, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'goResp_test.started')
                    # update status
                    goResp_test.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(goResp_test.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(goResp_test.clearEvents, eventType='keyboard')  # clear events on next screen flip
                
                # if goResp_test is stopping this frame...
                if goResp_test.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > goResp_test.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        goResp_test.tStop = t  # not accounting for scr refresh
                        goResp_test.tStopRefresh = tThisFlipGlobal  # on global time
                        goResp_test.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'goResp_test.stopped')
                        # update status
                        goResp_test.status = FINISHED
                        goResp_test.status = FINISHED
                if goResp_test.status == STARTED and not waitOnFlip:
                    theseKeys = goResp_test.getKeys(keyList=['left', 'right'], ignoreKeys=["escape"], waitRelease=False)
                    _goResp_test_allKeys.extend(theseKeys)
                    if len(_goResp_test_allKeys):
                        goResp_test.keys = _goResp_test_allKeys[0].name  # just the first key pressed
                        goResp_test.rt = _goResp_test_allKeys[0].rt
                        goResp_test.duration = _goResp_test_allKeys[0].duration
                        # was this correct?
                        if (goResp_test.keys == str(currentCorrectResponse)) or (goResp_test.keys == currentCorrectResponse):
                            goResp_test.corr = 1
                        else:
                            goResp_test.corr = 0
                
                # *stopSignal_test* updates
                
                # if stopSignal_test is starting this frame...
                if stopSignal_test.status == NOT_STARTED and tThisFlip >= SSDInput-frameTolerance:
                    # keep track of start time/frame for later
                    stopSignal_test.frameNStart = frameN  # exact frame index
                    stopSignal_test.tStart = t  # local t and not account for scr refresh
                    stopSignal_test.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(stopSignal_test, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stopSignal_test.started')
                    # update status
                    stopSignal_test.status = STARTED
                    stopSignal_test.setAutoDraw(True)
                
                # if stopSignal_test is active this frame...
                if stopSignal_test.status == STARTED:
                    # update params
                    pass
                
                # if stopSignal_test is stopping this frame...
                if stopSignal_test.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > stopSignal_test.tStartRefresh + .5-frameTolerance:
                        # keep track of stop time/frame for later
                        stopSignal_test.tStop = t  # not accounting for scr refresh
                        stopSignal_test.tStopRefresh = tThisFlipGlobal  # on global time
                        stopSignal_test.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'stopSignal_test.stopped')
                        # update status
                        stopSignal_test.status = FINISHED
                        stopSignal_test.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    test_trial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in test_trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "test_trial" ---
            for thisComponent in test_trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for test_trial
            test_trial.tStop = globalClock.getTime(format='float')
            test_trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('test_trial.stopped', test_trial.tStop)
            # check responses
            if goResp_test.keys in ['', [], None]:  # No response was made
                goResp_test.keys = None
                # was no response the correct answer?!
                if str(currentCorrectResponse).lower() == 'none':
                   goResp_test.corr = 1;  # correct non-response
                else:
                   goResp_test.corr = 0;  # failed to respond (incorrectly)
            # store data for testTrials (TrialHandler)
            testTrials.addData('goResp_test.keys',goResp_test.keys)
            testTrials.addData('goResp_test.corr', goResp_test.corr)
            if goResp_test.keys != None:  # we had a response
                testTrials.addData('goResp_test.rt', goResp_test.rt)
                testTrials.addData('goResp_test.duration', goResp_test.duration)
            # the Routine "test_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "ssdChange" ---
            # create an object to store info about Routine ssdChange
            ssdChange = data.Routine(
                name='ssdChange',
                components=[],
            )
            ssdChange.status = NOT_STARTED
            continueRoutine = True
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
            # store start times for ssdChange
            ssdChange.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            ssdChange.tStart = globalClock.getTime(format='float')
            ssdChange.status = STARTED
            thisExp.addData('ssdChange.started', ssdChange.tStart)
            ssdChange.maxDuration = None
            # keep track of which components have finished
            ssdChangeComponents = ssdChange.components
            for thisComponent in ssdChange.components:
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
            # if trial has changed, end Routine now
            if isinstance(testTrials, data.TrialHandler2) and thisTestTrial.thisN != testTrials.thisTrial.thisN:
                continueRoutine = False
            ssdChange.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    ssdChange.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ssdChange.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "ssdChange" ---
            for thisComponent in ssdChange.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for ssdChange
            ssdChange.tStop = globalClock.getTime(format='float')
            ssdChange.tStopRefresh = tThisFlipGlobal
            thisExp.addData('ssdChange.stopped', ssdChange.tStop)
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
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "endOfStopBlockFeedback" ---
        # create an object to store info about Routine endOfStopBlockFeedback
        endOfStopBlockFeedback = data.Routine(
            name='endOfStopBlockFeedback',
            components=[text_6, key_resp_4],
        )
        endOfStopBlockFeedback.status = NOT_STARTED
        continueRoutine = True
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
        # create starting attributes for key_resp_4
        key_resp_4.keys = []
        key_resp_4.rt = []
        _key_resp_4_allKeys = []
        # store start times for endOfStopBlockFeedback
        endOfStopBlockFeedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        endOfStopBlockFeedback.tStart = globalClock.getTime(format='float')
        endOfStopBlockFeedback.status = STARTED
        thisExp.addData('endOfStopBlockFeedback.started', endOfStopBlockFeedback.tStart)
        endOfStopBlockFeedback.maxDuration = None
        # keep track of which components have finished
        endOfStopBlockFeedbackComponents = endOfStopBlockFeedback.components
        for thisComponent in endOfStopBlockFeedback.components:
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
        # if trial has changed, end Routine now
        if isinstance(stopBlocks, data.TrialHandler2) and thisStopBlock.thisN != stopBlocks.thisTrial.thisN:
            continueRoutine = False
        endOfStopBlockFeedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 60.0:
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
            
            # if text_6 is stopping this frame...
            if text_6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_6.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    text_6.tStop = t  # not accounting for scr refresh
                    text_6.tStopRefresh = tThisFlipGlobal  # on global time
                    text_6.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_6.stopped')
                    # update status
                    text_6.status = FINISHED
                    text_6.setAutoDraw(False)
            
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
            
            # if key_resp_4 is stopping this frame...
            if key_resp_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_4.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_4.tStop = t  # not accounting for scr refresh
                    key_resp_4.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp_4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_4.stopped')
                    # update status
                    key_resp_4.status = FINISHED
                    key_resp_4.status = FINISHED
            if key_resp_4.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_4.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_4_allKeys.extend(theseKeys)
                if len(_key_resp_4_allKeys):
                    key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                    key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                    key_resp_4.duration = _key_resp_4_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                endOfStopBlockFeedback.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in endOfStopBlockFeedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "endOfStopBlockFeedback" ---
        for thisComponent in endOfStopBlockFeedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for endOfStopBlockFeedback
        endOfStopBlockFeedback.tStop = globalClock.getTime(format='float')
        endOfStopBlockFeedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('endOfStopBlockFeedback.stopped', endOfStopBlockFeedback.tStop)
        # check responses
        if key_resp_4.keys in ['', [], None]:  # No response was made
            key_resp_4.keys = None
        stopBlocks.addData('key_resp_4.keys',key_resp_4.keys)
        if key_resp_4.keys != None:  # we had a response
            stopBlocks.addData('key_resp_4.rt', key_resp_4.rt)
            stopBlocks.addData('key_resp_4.duration', key_resp_4.duration)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if endOfStopBlockFeedback.maxDurationReached:
            routineTimer.addTime(-endOfStopBlockFeedback.maxDuration)
        elif endOfStopBlockFeedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-60.000000)
        thisExp.nextEntry()
        
    # completed numTestBlocks repeats of 'stopBlocks'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "end" ---
    # create an object to store info about Routine end
    end = data.Routine(
        name='end',
        components=[ending_text, end_resp],
    )
    end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for end_resp
    end_resp.keys = []
    end_resp.rt = []
    _end_resp_allKeys = []
    # store start times for end
    end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    end.tStart = globalClock.getTime(format='float')
    end.status = STARTED
    thisExp.addData('end.started', end.tStart)
    end.maxDuration = None
    # keep track of which components have finished
    endComponents = end.components
    for thisComponent in end.components:
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
    end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 300.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *ending_text* updates
        
        # if ending_text is starting this frame...
        if ending_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ending_text.frameNStart = frameN  # exact frame index
            ending_text.tStart = t  # local t and not account for scr refresh
            ending_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ending_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ending_text.started')
            # update status
            ending_text.status = STARTED
            ending_text.setAutoDraw(True)
        
        # if ending_text is active this frame...
        if ending_text.status == STARTED:
            # update params
            pass
        
        # if ending_text is stopping this frame...
        if ending_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > ending_text.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                ending_text.tStop = t  # not accounting for scr refresh
                ending_text.tStopRefresh = tThisFlipGlobal  # on global time
                ending_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ending_text.stopped')
                # update status
                ending_text.status = FINISHED
                ending_text.setAutoDraw(False)
        
        # *end_resp* updates
        waitOnFlip = False
        
        # if end_resp is starting this frame...
        if end_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_resp.frameNStart = frameN  # exact frame index
            end_resp.tStart = t  # local t and not account for scr refresh
            end_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_resp.started')
            # update status
            end_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(end_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(end_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if end_resp is stopping this frame...
        if end_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > end_resp.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                end_resp.tStop = t  # not accounting for scr refresh
                end_resp.tStopRefresh = tThisFlipGlobal  # on global time
                end_resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'end_resp.stopped')
                # update status
                end_resp.status = FINISHED
                end_resp.status = FINISHED
        if end_resp.status == STARTED and not waitOnFlip:
            theseKeys = end_resp.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
            _end_resp_allKeys.extend(theseKeys)
            if len(_end_resp_allKeys):
                end_resp.keys = _end_resp_allKeys[-1].name  # just the last key pressed
                end_resp.rt = _end_resp_allKeys[-1].rt
                end_resp.duration = _end_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "end" ---
    for thisComponent in end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for end
    end.tStop = globalClock.getTime(format='float')
    end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('end.stopped', end.tStop)
    # check responses
    if end_resp.keys in ['', [], None]:  # No response was made
        end_resp.keys = None
    thisExp.addData('end_resp.keys',end_resp.keys)
    if end_resp.keys != None:  # we had a response
        thisExp.addData('end_resp.rt', end_resp.rt)
        thisExp.addData('end_resp.duration', end_resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if end.maxDurationReached:
        routineTimer.addTime(-end.maxDuration)
    elif end.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-300.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
