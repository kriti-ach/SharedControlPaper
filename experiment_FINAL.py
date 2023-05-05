from psychopy import visual, core, gui, data, core
from wooting_utils import WootingPython, HID_CODE_SPACE
import numpy as np
import sys
import wx
import random

app = wx.App(False)

PRESS_SCALER = 1 / 10

practice_clock = core.Clock()
testing_clock = core.Clock()

# constants with units in the visual degrees or degrees/loop
STARTING_POS = [-15, 0]
FINISH_LINE = 15
RING_PACE = (0.095, 0)

# constants with units in the seconds
COUNTDOWN_TIME = 1
FEEDBACK_TIME = 2.0
BREAK_TIME = 10.0
BLOCK_END_TIME = 10.0
PRACTICE_END_TIME = 5.0
MIN_SSD = 2
MAX_SSD = 4.9

INSTRUCTIONS = (
    "Welcome to the task!\n\n"
    + "On each trial, your job is to keep a dot inside of a moving ring by controlling its speed.\n\n"
    + "After a countdown, the ring will begin to move from left to right. Press the spacebar to move the dot.\n\n"
    + "The harder your press the spacebar, the faster the dot will move. Please try your best to keep the dot within the ring.\n\n"
    + "When the screen turns red, this indicates that you should stop the movement of the dot by quickly stopping your spacebar press.\n\n"
    + "On a subset of trials, the computer will intervene and stop the dot irrespective of your behavior.\n\n"
    + "Please try to keep the space bar pressed the entire time and try to not let go of the space bar unless the screen turns red. \n\n"
    + "The task is broken up into a practice phase of 20 trials and a testing phase consisting of 4 blocks. \n\n"
    + "You will get a break in the middle of each block. \n"
    + "When you are ready to begin the practice phase, press the spacebar."
)
END_TEXT = "Thank you. Please press the spacebar to end this task."
PRACTICE_INSTRUCTIONS_GO = (
    "First we will have you practice moving the ball across the screen.\n\n"
    + "Remember to try your best to keep the ball in the ring.\n\n"
)
PRACTICE_INSTRUCTIONS_STOP = (
    "Now we will have you practice stopping your movement.\n\n"
    + "Remember, when the screen turns red try to stop the movement\n\n"
    + "of the ball by quickly stopping your spacebar press."
)

# feedback text options
PRESSURE_FEEDBACK = "Remember to keep the space pressed throughout the trial."
LATE_FEEDBACK = "You are starting too late...\n Press the space bar as soon as the ring starts moving."

NO_PRESS_TEXT = "Keep space bar pressed!"
LATE_TEXT = "You are starting too late!"


def sample_SSD(scale=1):
    SSD = np.random.exponential(scale=scale) + MIN_SSD
    while SSD > MAX_SSD:
        SSD = np.random.exponential(scale=scale) + MIN_SSD
    return SSD


def getInput(id_text="s999", sess_text="001"):
    textBox = gui.Dlg(title="Experimenter Input")
    textBox.addField("Subject ID: ", id_text)
    textBox.addField("Session: ", sess_text)
    textBox.show()
    if textBox.OK:
        text1 = textBox.data[0]
        text2 = textBox.data[1]
        return text1, text2
    else:
        return text1, text2

    
def get_prob_dist_inputs(n_trials=20, block1=0.1, block2=0.9):
    while True:
        prob_dist = gui.Dlg(title="Probability Distribution of Conditions")
        prob_dist.addText('Enter total number of trials and % of AI trials in each block.')
        prob_dist.addText('There will be 2 blocks only. (0% AI and 90% AI.)')
        prob_dist.addText('Number of trials should be divisible by 2')
        prob_dist.addField('Number of Trials (Total): ', n_trials)
        prob_dist.addField('Block 1 AI % in proportions: ', block1)
        prob_dist.addField('Block 2 AI % in proportions: ', block2)
        prob_dist.show()

        if not prob_dist.OK:
            print('nothing was entered')
            break

        n_trials = prob_dist.data[0]
        block1 = prob_dist.data[1]
        block2 = prob_dist.data[2]

        if n_trials % 2 == 0:
            break
        else:
            print("Error - Please enter a number of total trials divisible by 2.")
    
    return n_trials, block1, block2

def create_conditions_array(stop_trials, ai_trials):
    conditions = np.array([0] * stop_trials + [1] * ai_trials)
    np.random.shuffle(conditions)
    conditions = conditions.astype('object')
    conditions[conditions == 0] = 'stop'
    conditions[conditions == 1] = 'ai'
    return conditions


def setup_trials():
    n_trials, block1, block2 = get_prob_dist_inputs()
    if n_trials == 0:
        return [], 0

    block = n_trials // 2
    ai_trials_block1 = int(block * block1)
    ai_trials_block2 = int(block * block2)
    stop_trials_block1 = block - ai_trials_block1
    stop_trials_block2 = block - ai_trials_block2

    conditions_block1 = create_conditions_array(stop_trials_block1, ai_trials_block1)
    conditions_block2 = create_conditions_array(stop_trials_block2, ai_trials_block2)

    if random.randint(0, 1) == 0:
        conditions = list(conditions_block1) + list(conditions_block2)
    else:
        conditions = list(conditions_block2) + list(conditions_block1)

    return conditions, block


def setupPractice(num_stop=1, num_ai=9):
    practice_conditions = ["stop"] * num_stop + ["ai"] * num_ai
    np.random.shuffle(practice_conditions)

    return practice_conditions, len(practice_conditions)


if __name__ == "__main__":
    # SET UP WOOTING KB
    print("setting up kb")
    wp = WootingPython()
    wp.initialise()
    wp.is_initialised()
    wp.get_info()
    print("> Checking if keyboard is connected...")
    if not wp.is_connected():
        print("> ERROR: No keyboard found! Connect it and try again.")
        sys.exit(-1)

    # subject info
    conditions, block = setup_trials()
    practice, practice_len = setupPractice()
    subid, sess = getInput()

    # Trial Setup
    stims = practice + conditions
    stimlist = [{"condition": i} for i in stims]
    trials = data.TrialHandler(
        stimlist,
        1,
        method="sequential",
        extraInfo={"participant": subid, "session": sess},
    )

    # create a window
    mywin = visual.Window(monitor="testMonitor", units="deg", fullscr=True)

    # CONSTANT TEXT
    intro_stim = visual.TextStim(
        win=mywin, text=INSTRUCTIONS, height=0.85, pos=[0, 0], wrapWidth=30
    )
    end_stim = visual.TextStim(win=mywin, text=END_TEXT, height=0.75, pos=[0, 0])
    feedback = visual.TextStim(
        win=mywin, text="Trial Complete", height=1.5, pos=[0, -5]
    )
    late_start_alert = visual.TextStim(win=mywin, text=LATE_TEXT, height=1, pos=[0, 6])
    no_pressure_alert = visual.TextStim(
        win=mywin, text=NO_PRESS_TEXT, height=1, pos=[0, 7]
    )
    break_feedback = visual.TextStim(
        win=mywin, text="Take a 10 second break", height=1.5, pos=[0, 3.5]
    )
    block_feedback = visual.TextStim(
        win=mywin,
        text="Block 1 Complete! \n Block 2 will start after a 10 second break...",
        height=1.5,
        pos=[0, 3.5],
    )
    practice_end = visual.TextStim(
        win=mywin,
        text="Please review your feedback, testing will begin shortly...",
        height=1,
        pos=[0, 3],
        wrapWidth=30,
    )
    practice_feedback_pressure = visual.TextStim(
        win=mywin, text=PRESSURE_FEEDBACK, height=0.7, pos=[0, 0], wrapWidth=50
    )
    practice_feedback_late = visual.TextStim(
        win=mywin, text=LATE_FEEDBACK, height=0.7, pos=[0, -2], wrapWidth=50
    )
    practice_go = visual.TextStim(
        win=mywin, text=PRACTICE_INSTRUCTIONS_GO, height=0.7, pos=[0, -2], wrapWidth=50
    )
    practice_stop = visual.TextStim(
        win=mywin, text=PRACTICE_INSTRUCTIONS_STOP, height=0.7, pos=[0, -2], wrapWidth=50
    )

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
    
    # Init stimuli
    waitingForSpace = True
    Hit = False
    FinishLine = False
    stillMoving = True
    countdown = visual.TextStim(win=mywin, text="", height=1, pos=[0, 0])
    fixation = visual.TextStim(
        win=mywin, text="+", height=5, color=[255, 255, 255], pos=[0, 0]
    )  
    
    # FIXATION
    ring = visual.Circle(
        win=mywin,
        radius=2,
        edges=32,
        pos=STARTING_POS,
        lineWidth=15,
        lineColor="white",
        fillColor=None,
    )
    
    ball = visual.Circle(
        win=mywin,
        radius=0.8,
        edges=32,
        pos=STARTING_POS,
        lineWidth=10,
        lineColor="white",
        fillColor="white",
    )
    
    stopsignal = visual.Rect(
        win=mywin,
        width=5,
        height=5,
        pos=(0, 0),
        lineWidth=50,
        lineColor="white",
        fillColor=None,
    )
    finishline = visual.Line(
        win=mywin,
        lineWidth=2,
        start=(FINISH_LINE + ring.radius, -20),
        end=(FINISH_LINE + ring.radius, 20),
    )
    
    # Go Practice
    practice_go.draw()
    
    trial_start = core.getTime()
    # Countdown / ITI
    timer = core.CountdownTimer(COUNTDOWN_TIME)
    while timer.getTime() > 0:  # after 5s will become negative
        countdown.text = f"{timer.getTime():.0f}"
        ball.draw()
        ring.draw()
        fixation.draw()
        finishline.draw()
        mywin.flip()
            
    while not FinishLine:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        ring.pos += RING_PACE
        if analog_codes:
            ball.pos += (np.max(analog_codes) * PRESS_SCALER, 0)
        
        dist = ball.pos[0] - ring.pos[0]
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
        practice_stop.draw()
        finishline.draw()
        mywin.flip()
                
    # TRIAL LOOP
    for count, trial in enumerate(trials):
        if count == 0:
            practice_clock.reset()

        if count == practice_len:
            testing_clock.reset()

        if count == practice_len + (block / 2) or count == practice_len + (
            (block / 2) + block
        ):
            break_timer = core.CountdownTimer(BREAK_TIME)
            while break_timer.getTime() > 0:
                mywin.color = "grey"
                break_feedback.draw()
                mywin.flip()

        # Init stimuli
        countdown = visual.TextStim(win=mywin, text="", height=1, pos=[0, 0])
        fixation = visual.TextStim(
            win=mywin, text="+", height=5, color=[255, 255, 255], pos=[0, 0]
        )  # FIXATION
        ring = visual.Circle(
            win=mywin,
            radius=2,
            edges=32,
            pos=STARTING_POS,
            lineWidth=15,
            lineColor="white",
            fillColor=None,
        )
        ball = visual.Circle(
            win=mywin,
            radius=0.8,
            edges=32,
            pos=STARTING_POS,
            lineWidth=10,
            lineColor="white",
            fillColor="white",
        )
        stopsignal = visual.Rect(
            win=mywin,
            width=5,
            height=5,
            pos=(0, 0),
            lineWidth=50,
            lineColor="white",
            fillColor=None,
        )
        finishline = visual.Line(
            win=mywin,
            lineWidth=2,
            start=(FINISH_LINE + ring.radius, -20),
            end=(FINISH_LINE + ring.radius, 20),
        )

        # Init Trial Data
        SSD = sample_SSD()
        trials.data.add("SSD", SSD)
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
            countdown.text = f"{timer.getTime():.0f}"
            ball.draw()
            ring.draw()
            fixation.draw()
            finishline.draw()
            mywin.flip()

        # START
        if trial["condition"] == "stop":
            trial_start = core.getTime()
            # SSD
            SSD_timer = core.CountdownTimer(SSD)
            while SSD_timer.getTime() > 0:
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
            while end_trial_timer.getTime() > 0:
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

                mywin.color = "red"
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            feedback_timer = core.CountdownTimer(FEEDBACK_TIME)
            while feedback_timer.getTime() > 0:
                mywin.color = "grey"
                ball.draw()
                ring.draw()
                finishline.draw()
                feedback.draw()

                # for practice
                unique, counts = np.unique(pressures[15:-15], return_counts=True)
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

                percent_zeros = zeros / pressure_len
                percent_ones = ones / pressure_len

                if count < practice_len:
                    if percent_zeros >= 0.3:
                        no_pressure_alert.draw()
                        feedback_tracker.append("pressure")

                    if np.mean(pressures[:15]) == 0:
                        late_start_alert.draw()
                        feedback_tracker.append("late")

                mywin.flip()

        elif trial["condition"] == "ai":
            trial_start = core.getTime()
            # SSD
            SSD_timer = core.CountdownTimer(SSD)
            while SSD_timer.getTime() > 0:
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
            while end_trial_timer.getTime() > 0:
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

                mywin.color = "red"
                ball.draw()
                ring.draw()
                finishline.draw()
                mywin.flip()

            feedback_timer = core.CountdownTimer(FEEDBACK_TIME)
            while feedback_timer.getTime() > 0:
                mywin.color = "grey"
                ball.draw()
                ring.draw()
                finishline.draw()
                feedback.draw()

                # for practice
                unique, counts = np.unique(pressures[15:-15], return_counts=True)
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

                percent_zeros = zeros / pressure_len
                percent_ones = ones / pressure_len

                if count < practice_len:
                    if percent_zeros >= 0.3:
                        no_pressure_alert.draw()
                        feedback_tracker.append("pressure")

                    if np.mean(pressures[:15]) == 0:
                        late_start_alert.draw()
                        feedback_tracker.append("late")

                mywin.flip()

        # Save Data
        trials.data.add("time_stamps", " ".join([str(elem) for elem in timings]))
        trials.data.add("pressures", " ".join([str(elem) for elem in pressures]))
        trials.data.add("distances", " ".join([str(elem) for elem in distances]))

        if count < practice_len:
            trials.data.add("block", "practice")
            trials.data.add("phase", "practice")
        elif practice_len <= count and count < practice_len + block:
            trials.data.add("block", "block 1")
            trials.data.add("phase", "test")
        elif practice_len + block <= count:
            trials.data.add("block", "block 2")
            trials.data.add("phase", "test")

        if count + 1 == practice_len + block:
            block_end_timer = core.CountdownTimer(BLOCK_END_TIME)
            while block_end_timer.getTime() > 0:
                mywin.color = "grey"
                block_feedback.draw()
                mywin.flip()
        elif count + 1 == practice_len:
            practice_end_timer = core.CountdownTimer(PRACTICE_END_TIME)
            practice_duration = practice_clock.getTime()

            while practice_end_timer.getTime() > 0:
                mywin.color = "grey"
                practice_end.draw()
                if "late" in set(feedback_tracker):
                    practice_feedback_late.draw()

                if "pressure" in set(feedback_tracker):
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

    testing_duration = testing_clock.getTime()
    trials.saveAsText(fileName="data_sub-%s_ses-%s" % (subid, sess), delim=",")
    print(f"Practice phase duration: {practice_duration} seconds")
    print(f"Testing phase duration: {testing_duration} seconds")

    # Cleanup
    mywin.close()
    core.quit()
