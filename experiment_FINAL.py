from psychopy import visual, core, gui, data
from wooting_utils import WootingPython, HID_CODE_SPACE
import numpy as np
import sys
import wx
import random

app = wx.App(False)

PRESS_SCALER = 1 / 10

# constants with units in the visual degrees or degrees/loop
STARTING_POS = [-15, 0]
FINISH_LINE = 15
RING_PACE = (0.085, 0)

# constants with units in the seconds
COUNTDOWN_TIME = 1
FEEDBACK_TIME = 2.0
BREAK_TIME = 10.0
BLOCK_END_TIME = 10.0
PRACTICE_END_TIME = 5.0
MIN_SSD = 2
MAX_SSD = 4.9

INSTRUCTIONS = 'Welcome to the task!\n\n' +\
    'On each trial, your job is to keep a ball inside of a moving ring by controlling its speed.\n\n' +\
    'After a countdown, the ring will begin to move from left to right. Press the spacebar to move the ball.\n\n' +\
    'The harder your press the spacebar, the faster the ball will move. Please try your best to keep the ball within the ring.\n\n' +\
    'The background will turn red. If the background turns red, please stop moving the ball as quickly as possible.\n\n' +\
    'On some trials the ball will freeze and stop as soon as the background turns red. \n' +\
    'Please try to keep the space bar pressed the entire time and try to not let go of the space bar. \n\n' +\
    'The task is broken up into a practice phase of 20 trials and a testing phase consisting of 2 blocks (200 trials each). \n\n' +\
    'You will get a break in the middle of each block. \n' +\
    'When you are ready to begin the practice phase, press the spacebar.'
END_TEXT = 'Thank you. Please press the spacebar to end this task.'

# feedback text options
PRESSURE_FEEDBACK = 'Remember to keep the space pressed throughout the trial.'
LATE_FEEDBACK = 'You are starting too late...\n Press the space bar as soon as the ring starts moving.'

NO_PRESS_TEXT = "Keep space bar pressed!"
LATE_TEXT = "You are starting too late!"


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


def setupTrials(block1=0.1, block2=.90, n_text=20):
    prob_dist = gui.Dlg(title="Probability Distribution of Conditions")
    prob_dist.addText('Enter total number of trials and % of AI trials in each block.')
    prob_dist.addText('There will be 2 blocks only. (0% AI and 90% AI.)')
    prob_dist.addText('Number of trials should be divisible by 2')
    prob_dist.addField('Number of Trials (Total): ', n_text)
    prob_dist.addField('Block 1 AI % in proportions: ', block1)
    prob_dist.addField('Block 2 AI % in proportions: ', block2)
    prob_dist.show()
    if prob_dist.OK:
        nTrials = prob_dist.data[0]
        block1 = prob_dist.data[1]
        block2 = prob_dist.data[2]
    else:
        print('nothing was entered')

    assert nTrials != 0
    
    while nTrials % 2 != 0:
        prob_dist = gui.Dlg(title="Probability Distribution of Conditions")
        prob_dist.addText('Error - Please enter a number of total trials divisible by 2.')
        prob_dist.addText('Enter total number of trials and % of AI trials in each block.')
        prob_dist.addText('There will be 2 blocks only. (0% AI and 90% AI.)')
        prob_dist.addText('Number of trials should be divisible by 2')
        prob_dist.addField('Number of Trials (Total): ', n_text)
        prob_dist.addField('Block 1 AI % in proportions: ', block1)
        prob_dist.addField('Block 2 AI % in proportions: ', block2)
        prob_dist.show()
        if prob_dist.OK:
            nTrials = prob_dist.data[0]
            block1 = prob_dist.data[1]
            block2 = prob_dist.data[2]
        else:
            print('nothing was entered')
        
    block = nTrials / 2

    # Obtaining number of each condition
    aiTrials_block1 = int(block * block1)
    stopTrials_block1 = block - aiTrials_block1
    aiTrials_block2 = int(block * block2)
    stopTrials_block2 = block - aiTrials_block2
        
    assert nTrials == (aiTrials_block1 + stopTrials_block1 + aiTrials_block2 + stopTrials_block2)

    # Creating array of conditions then shuffling
    conditions_block1 = np.array([0] * int(stopTrials_block1) + [1] * int(aiTrials_block1))
    np.random.shuffle(conditions_block1)
    
    # Replacing values with trial types
    conditions_block1 = conditions_block1.astype('object')
    conditions_block1[conditions_block1 == 0] = 'stop'
    conditions_block1[conditions_block1 == 1] = 'ai'
    
    # Creating array of conditions then shuffling
    conditions_block2 = np.array([0] * int(stopTrials_block2) + [1] * int(aiTrials_block2))
    np.random.shuffle(conditions_block2)
    
    # Replacing values with trial types
    conditions_block2 = conditions_block2.astype('object')
    conditions_block2[conditions_block2 == 0] = 'stop'
    conditions_block2[conditions_block2 == 1] = 'ai'
    
    
    # randomizing the blocks
    if random.randint(0, 1) == 0:
        conditions = list(conditions_block1) + list(conditions_block2)
    else:
        conditions = list(conditions_block2) + list(conditions_block1)

    return conditions, block

def setupPractice():
    practice_block = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    
    #practice_block = np.array([0, 1])
    
    np.random.shuffle(practice_block)
    
    # Replacing values with trial types
    practice_block = practice_block.astype('object')
    practice_block[practice_block == 0] = 'stop'
    practice_block[practice_block == 1] = 'ai'
    
    return list(practice_block), len(practice_block)
    

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

    # subject info
    conditions, block = setupTrials()
    practice, practice_len = setupPractice()
    subid, sess = getInput()
    
    # Trial Setup
    stims = practice + conditions
    stimlist = [{'condition': i} for i in stims]
    trials = data.TrialHandler(stimlist, 1, method='sequential',
                                   extraInfo={'participant': subid,
                                              'session': sess})

    # create a window
    mywin = visual.Window(monitor='testMonitor',
                          units="deg", fullscr=True)
    

    # CONSTANT TEXT
    intro_stim = visual.TextStim(win=mywin, text=INSTRUCTIONS, height=.85, pos=[0, 0], wrapWidth=30)
    end_stim = visual.TextStim(win=mywin, text=END_TEXT, height=.75, pos=[0, 0])
    feedback = visual.TextStim(win=mywin, text='Trial Complete',
                               height=1.5, pos=[0, -5])
    late_start_alert = visual.TextStim(win=mywin, text=LATE_TEXT,
                               height=1, pos=[0, 6])
    no_pressure_alert = visual.TextStim(win=mywin, text=NO_PRESS_TEXT,
                               height=1, pos=[0, 7])
    break_feedback = visual.TextStim(win=mywin, text='Take a 10 second break',
                               height=1.5, pos=[0, 3.5])
    block_feedback = visual.TextStim(win=mywin, text='Block 1 Complete! \n Block 2 will start after a 10 second break...',
                               height=1.5, pos=[0, 3.5])
    practice_end = visual.TextStim(win=mywin, text='Please review your feedback, testing will begin shortly...',
                               height=1, pos=[0, 3], wrapWidth = 30)
    practice_feedback_pressure = visual.TextStim(win=mywin, text=PRESSURE_FEEDBACK,
                               height=.7, pos=[0, 0], wrapWidth = 50)
    practice_feedback_late = visual.TextStim(win=mywin, text=LATE_FEEDBACK,
                               height=.7, pos=[0, -2], wrapWidth = 50)

    # Practice Feedback Count
    feedback_tracker = []

    # INSTRUCTIONS
    intro_stim.draw()
    mywin.flip()
    waitingForSpace = True
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_SPACE in scan_codes:
            waitingForSpace = False
        
        
    # TRIAL LOOP
    for count, trial in enumerate(trials):
        if count == practice_len + (block/2) or count == practice_len + ((block/2) + block):
            break_timer = core.CountdownTimer(BREAK_TIME)
            while break_timer.getTime() > 0:
                mywin.color = 'grey'
                break_feedback.draw()
                mywin.flip()
                
        # Init stimuli
        countdown = visual.TextStim(win=mywin, text='', height=1, pos=[0, 0])
        fixation = visual.TextStim(win=mywin, text='+', height = 5, color=[255, 255, 255], pos = [0,0]) # FIXATION
        ring = visual.Circle(win=mywin, radius=2, edges=32, pos=STARTING_POS,
                             lineWidth=15, lineColor='white', fillColor=None)
        ball = visual.Circle(win=mywin, radius=.8, edges=32,
                             pos=STARTING_POS, lineWidth=10, lineColor='white',
                             fillColor='white')
        stopsignal = visual.Rect(win=mywin, width=5, height=5, pos=(0, 0),
                                 lineWidth=50, lineColor='white', fillColor=None)
        finishline = visual.Line(win=mywin, lineWidth=2, start=(FINISH_LINE + ring.radius, -20), end=(FINISH_LINE + ring.radius, 20))

        # Init Trial Data
        SSD = sample_SSD()
        trials.data.add('SSD', SSD)
        waitingForSpace = True
        Hit = False
        FinishLine = False
        stillMoving = True
        pressures = []
        distances = []
        timings = []

        # Countdown / ITI
        timer = core.CountdownTimer(COUNTDOWN_TIME)
        while timer.getTime() > 0:  # after 5s will become negative
            countdown.text = f'{timer.getTime():.0f}'
            ball.draw()
            ring.draw()
            #countdown.draw()
            fixation.draw()
            finishline.draw()
            mywin.flip()
        
        # this uses the fixation mark
        
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
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            # StopSignal
            end_trial_timer = core.CountdownTimer(1.5)
            while (end_trial_timer.getTime() > 0):
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

                mywin.color = 'red'
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
                
                # for practice
                unique, counts = np.unique(pressures, return_counts=True)
                feedback_data = dict(zip(unique, counts))
                pressure_len = len(pressures)
                if 0 in feedback_data.keys():
                    zeros = feedback_data[0]
                else:
                    zeros = 0
                if 1 in feedback_data.keys():
                    ones = feedback_data[1]
                else:
                    ones = 0

                percent_zeros = zeros/pressure_len
                percent_ones = ones/pressure_len

                if count < practice_len:
                    if percent_zeros >= .3:
                        no_pressure_alert.draw()
                        feedback_tracker.append('pressure')
                        
                    if np.mean(pressures[:10]) == 0:
                        late_start_alert.draw()
                        feedback_tracker.append('late')
                    
                mywin.flip()

        elif trial['condition'] == 'ai':
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
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            # StopSignal
            end_trial_timer = core.CountdownTimer(1.5)
            while (end_trial_timer.getTime() > 0):
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                if analog_codes:
                    not_moving_timer = core.CountdownTimer(1)
                    ball.pos == (np.max(analog_codes) * PRESS_SCALER, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)

                dist = ball.pos[0] - ring.pos[0]
                distances.append(dist)
                if dist > 1.05:
                    Hit = True

                #stopsignal.draw()
                mywin.color = 'red'
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
                
                # for practice
                unique, counts = np.unique(pressures, return_counts=True)
                feedback_data = dict(zip(unique, counts))
                pressure_len = len(pressures)
                if 0 in feedback_data.keys():
                    zeros = feedback_data[0]
                else:
                    zeros = 0
                if 1 in feedback_data.keys():
                    ones = feedback_data[1]
                else:
                    ones = 0
                    
                percent_zeros = zeros/pressure_len
                percent_ones = ones/pressure_len
                
                if count < practice_len:
                    if percent_zeros >= .3:
                        no_pressure_alert.draw()
                        feedback_tracker.append('pressure')
                        
                    if np.mean(pressures[:10]) == 0:
                        late_start_alert.draw()
                        feedback_tracker.append('late')
                        
                mywin.flip()

        # Save Data
        trials.data.add('time_stamps',
                        ' '.join([str(elem) for elem in timings]))
        trials.data.add('pressures',
                        ' '.join([str(elem) for elem in pressures]))
        trials.data.add('distances',
                        ' '.join([str(elem) for elem in distances]))
        
        if count < practice_len:
            trials.data.add('block', 'practice')
            trials.data.add('phase', 'practice')
        elif practice_len <= count and count < practice_len + block:
            trials.data.add('block', 'block 1')
            trials.data.add('phase', 'test')
        elif practice_len + block <= count:
            trials.data.add('block', 'block 2')
            trials.data.add('phase', 'test')
        
        if (count + 1 == practice_len+block):
            block_end_timer = core.CountdownTimer(BLOCK_END_TIME)
            while block_end_timer.getTime() > 0:
                mywin.color = 'grey'
                block_feedback.draw()
                mywin.flip()
        elif count + 1 == practice_len:
            practice_end_timer = core.CountdownTimer(PRACTICE_END_TIME)
            while practice_end_timer.getTime() > 0:
                mywin.color = 'grey'
                practice_end.draw()
                if 'late' in set(feedback_tracker):
                    practice_feedback_late.draw()
                
                if 'pressure' in set(feedback_tracker):
                    practice_feedback_pressure.draw()
                    
                mywin.flip()

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
