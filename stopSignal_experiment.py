from psychopy import visual, core, gui, data
from wooting_utils import WootingPython, HID_CODE_SPACE
import numpy as np
import random
import sys

import wx
app = wx.App(False)

PRESS_SCALER = 1 / 10

# constants with units in the visual degrees or degrees/loop
STARTING_POS = [-15, 0]
FINISH_LINE = 15
RING_PACE = (0.085, 0)

# constants with units in the seconds
COUNTDOWN_TIME = 3
FEEDBACK_TIME = 2.0
MIN_SSD = 2
MAX_SSD = 4.9

INSTRUCTIONS = 'Welcome to the task!\n\n' +\
    'In this task you will see shapes appear on the screen one at a time\n\n' +\
    'Only one response is correct for each shape.\n\n' +\
    'If the shape is a square, press your right finger.\n\n' +\
    'If the circle is a square, press your left finger.\n\n' +\
    'You should respond as quickly and accurately as possible to each shape.\n\n' +\
    'On some trials, a star will appear around the shape.  The star will appear with, or shortly after the shape appears.\n\n' +\
    'If you see a star appear, please try your best to withhold your response on that trial.\n\n' +\
    'If the star appears on a trial, and you try your best to withhold your response, you will find that you will be able to stop sometimes but not always.\n\n' +\
    'Please do not slow down your responses in order to wait for the star.  Continue to respond as quickly and accurately as possible.\n\n' +\
    'We will start practice when you finish instructions. Please make sure you understand the rules before moving on. During practice, you will see a reminder of the rules.\n\n' +\
    'This will be removed for test.\n\n' +\
    'When you are ready to begin, press the spacebar.'
END_TEXT = 'Thank you. Please press the spacebar to end this task.'

SHAPES = ["circle", "circle", "square", "square"]
TOTAL_SHAPES_USED = 4
STOP_SIGNAL_CONDITIONS = ["go", "go", "stop"]

POSSIBLE_RESPONSES = [
  ["Z key", 90],
  ["Z key", 90],
  ["M key", 77],
  ["M key", 77],
]

exp_len = 12
numTrialsPerBlock = 12
numTestBlocks = exp_len / numTrialsPerBlock


def sample_SSD(scale=1):
    SSD = np.random.exponential(scale=scale) + MIN_SSD
    while SSD > MAX_SSD:
        SSD = np.random.exponential(scale=scale) + MIN_SSD
    return SSD


def getInput(id_text="s999", sess_text='001'):
    textBox = gui.Dlg(title='Experimenter Input')
    textBox.addField('Subject ID: ', id_text)
    textBox.addField('Session: ', sess_text)
    textBox.show()
    if textBox.OK:
        text1 = textBox.data[0]
        text2 = textBox.data[1]
        return text1, text2
    else:
        return text1, text2


def getProbDist(go_text=.5, stop_text=.5, n_text=10):
    prob_dist = gui.Dlg(title="Probability Distribution of Conditions")
    prob_dist.addText('Enter the probability of each condition and number of trials.')
    prob_dist.addText('Trial types should add to 1.0')
    prob_dist.addField('Number of Trials (Total): ', n_text)
    prob_dist.addField('Go Trials: ', go_text)
    prob_dist.addField('Stop Trials: ', stop_text)
    prob_dist.show()
    if prob_dist.OK:
        nTrials = prob_dist.data[0]
        go = prob_dist.data[1]
        stop = prob_dist.data[2]
    else:
        print('nothing was entered')

    # Obtaining number of each condition
    goTrials = round(nTrials * go)
    stopTrials = round(nTrials * stop)

    assert nTrials == (goTrials + stopTrials)

    # Creating array of conditions then shuffling
    conditions = np.array([0] * goTrials + [1] * stopTrials)
    np.random.shuffle(conditions)

    # Replacing values with trial types
    conditions = conditions.astype('object')
    conditions[conditions == 0] = 'go'
    conditions[conditions == 1] = 'stop'

    return conditions

def createTrialTypes(numTrialsPerBlock, TOTAL_SHAPES_USED, SHAPES):
    unique_combos = len(STOP_SIGNAL_CONDITIONS) * TOTAL_SHAPES_USED;
    
    stims = []
    for x in range(len(STOP_SIGNAL_CONDITIONS)):
        for j in range(TOTAL_SHAPES_USED):
            stim = {
                'stim': SHAPES[j],
                'correct_response': POSSIBLE_RESPONSES[j][1],
                'stop_signal_condition': STOP_SIGNAL_CONDITIONS[x]
            }
            stims.append(stim)
    
    iteration = numTrialsPerBlock / unique_combos;
    
    shuffled_stims = random.sample(stims, len(stims))
    stims = shuffled_stims * iteration
    return stims


if __name__ == "__main__":
    # SET UP WOOTING KB
    print('setting up kb')
    wp = WootingPython()
    wp.initialise()
    wp.is_initialised()
    wp.get_info()
    print('> Checking if keyboard is connected...')
    if not wp.is_connected():
        print('> ERROR: No keyboard found! Connect it and try again.')
        sys.exit(-1)

    # subject/trial info
    #conditions = getProbDist()
    subid, sess = getInput()

    # create a window
    mywin = visual.Window(monitor="testMonitor",
                          units="deg", fullscr=True)
    # Trial Setup
    stims = createTrialTypes(numTrialsPerBlock, TOTAL_SHAPES_USED, SHAPES)
    stimlist = [{'condition': i} for i in stims]
    trials = data.TrialHandler(stimlist, 1, method='random',
                               extraInfo={'participant': subid,
                                          'session': sess})

    # CONSTANT TEXT
    intro_stim = visual.TextStim(
            win=mywin,
            text=INSTRUCTIONS,
            height=.85, pos=[0, 0],
            wrapWidth=30)
    end_stim = visual.TextStim(
            win=mywin,
            text=END_TEXT,
            height=.75, pos=[0, 0])
    feedback = visual.TextStim(win=mywin, text='Trial Complete',
                               height=1.5, pos=[0, 3.5])

    # INSTRUCTIONS
    intro_stim.draw()
    mywin.flip()
    waitingForSpace = True
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_SPACE in scan_codes:
            waitingForSpace = False

    # TRIAL LOOP
    for trial in trials:
        # Init stimuli
        fixation = visual.TextStim(win=mywin, text="+", height=5, color=[255, 255, 255], pos=[0, 0])
        square = visual.Rect(win=mywin, width=5, height=5,
                             pos=STARTING_POS, lineWidth=10, lineColor='black',
                             fillColor='black')
        circle = visual.Circle(win=mywin, radius=.8, edges=32,
                             pos=STARTING_POS, lineWidth=10, lineColor='black',
                             fillColor='black')
        stopsignal = visual.Polygon(win=mywin, radius=1, edges=5, pos=(0, 0),
                                 lineWidth=50, lineColor='white', fillColor=None)

        # Init Trial Data
        #SSD = sample_SSD()
        trials.data.add('SSD', SSD)
        waitingForSpace = True
        Hit = False
        pressures = []
        distances = []
        timings = []

        # Countdown / ITI
        timer = core.CountdownTimer(COUNTDOWN_TIME)
        while timer.getTime() > 0:  # after 5s will become negative
            fixation.draw()
            mywin.flip()

        # START
        if trial['condition'] == 'stop':
            trial_start = core.getTime()
            # SSD
            SSD_timer = core.CountdownTimer(SSD)
            while (SSD_timer.getTime() > 0):
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                ring.pos += RING_PACE
                if analog_codes:
                    ball.pos += (np.max(analog_codes) * PRESS_SCALER, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)
                dist = ball.pos[0] - ring.pos[0]
                distances.append(dist)
                if dist > 1.05:
                    Hit = True
                if np.abs(ring.pos[0]) >= FINISH_LINE:
                    FinishLine = True
                # fixation.draw()
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            # StopSignal
            end_trial_timer = core.CountdownTimer(1)
            not_moving_timer = core.CountdownTimer(1)
            while (end_trial_timer.getTime() > 0) or\
                    (not_moving_timer.getTime() > 0):
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                if analog_codes:
                    not_moving_timer = core.CountdownTimer(1)
                    ball.pos += (np.max(analog_codes) * PRESS_SCALER, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)

                dist = ball.pos[0] - ring.pos[0]
                distances.append(dist)
                if dist > 1.05:
                    Hit = True

                #stopsignal.draw()
                mywin.color = "red"
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            feedback_timer = core.CountdownTimer(FEEDBACK_TIME)
            while feedback_timer.getTime() > 0:
                mywin.color = 'grey'
                ball.draw()
                ring.draw()
                finishline.draw()
                feedback.draw()
                mywin.flip()
                
        elif trial['condition'] == 'go':
            trial_start = core.getTime()

            while not FinishLine:
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                
                if analog_codes:
                    ball.pos += (np.max(analog_codes) * PRESS_SCALER, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)
                dist = ball.pos[0] - ring.pos[0]
                distances.append(dist)
                if dist > 1.05:
                    Hit = True
                if np.abs(ring.pos[0]) >= FINISH_LINE:
                    FinishLine = True
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            feedback_timer = core.CountdownTimer(FEEDBACK_TIME)
            while feedback_timer.getTime() > 0:
                ball.draw()
                ring.draw()
                feedback.draw()
                finishline.draw()
                mywin.flip()

        # Save Data
        trials.data.add('time_stamps',
                        ' '.join([str(elem) for elem in timings]))
        trials.data.add('pressures',
                        ' '.join([str(elem) for elem in pressures]))
        trials.data.add('distances',
                        ' '.join([str(elem) for elem in distances]))

    # FINISH
    end_stim.draw()
    mywin.flip()
    waitingForSpace = True
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_SPACE in scan_codes:
            waitingForSpace = False

    trials.saveAsText(fileName='data_sub-%s_ses-%s' % (subid, sess), delim=',')
    # Cleanup
    mywin.close()
    core.quit()

