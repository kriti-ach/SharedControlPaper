from psychopy import visual, core, gui, data
from wooting_utils import WootingPython, HID_CODE_SPACE
import numpy as np
import sys



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
    'On each trial, your job is to keep a ball inside of a moving ring by controlling its speed.\n\n' +\
    'After a countdown, the ring will begin to move from left to right. Press the sbacebar to move the ball.\n\n' +\
    'The harder your press the spacebar, the faster the ball will move. Please try your best to keep the ball within the ring.\n\n' +\
    'On some trials, a box will appear around the ring. If the box appears, please stop moving the ball as quickly as possible.\n\n' +\
    'When you are ready to begin, press the spacebar.'
END_TEXT = 'Thank you. Please press the spacebar to end this task.'


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
    subid, sess = getInput()

    # create a window
    mywin = visual.Window(monitor="testMonitor",
                          units="deg", fullscr=True)
    # Trial Setup
    stims = ['go', 'go', 'go', 'go', 'stop', 'stop'] * 1
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
        countdown = visual.TextStim(win=mywin, text='', height=1, pos=[0, 0])
        ring = visual.Circle(win=mywin, radius=2, edges=32, pos=STARTING_POS,
                             lineWidth=15, lineColor='white')
        ball = visual.Circle(win=mywin, radius=.8, edges=32,
                             pos=STARTING_POS, lineWidth=10, lineColor='white',
                             fillColor='white')
        stopsignal = visual.Rect(win=mywin, width=5, height=5, pos=(0, 0),
                                 lineWidth=50, lineColor='white')
        finishline = visual.Line(win=mywin, lineWidth=2,
                                 start=(FINISH_LINE+ring.radius, -12.5),
                                 end=(FINISH_LINE+ring.radius, 12.5))

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
            countdown.draw()
            finishline.draw()
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
                    ball.pos += (np.max(analog_codes)/10, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)
                dist = ball.pos[0]-ring.pos[0]
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
            stopsignal.pos = ring.pos
            end_trial_timer = core.CountdownTimer(1)
            not_moving_timer = core.CountdownTimer(1)
            while (end_trial_timer.getTime() > 0) or\
                    (not_moving_timer.getTime() > 0):
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                if analog_codes:
                    not_moving_timer = core.CountdownTimer(1)
                    ball.pos += (np.max(analog_codes)/10, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)

                dist = ball.pos[0]-ring.pos[0]
                distances.append(dist)
                if dist > 1.05:
                    Hit = True

                stopsignal.draw()
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            feedback_timer = core.CountdownTimer(FEEDBACK_TIME)
            while feedback_timer.getTime() > 0:
                stopsignal.draw()
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
                ring.pos += RING_PACE
                if analog_codes:
                    ball.pos += (np.max(analog_codes)/10, 0)
                    pressures.append(np.max(analog_codes))
                else:
                    pressures.append(0)
                dist = ball.pos[0]-ring.pos[0]
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
