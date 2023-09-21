from psychopy import visual, core, gui, data, core
from wooting_utils import WootingPython, HID_CODE_SPACE, HID_CODE_ENTER
import numpy as np
import sys
import wx
import random
import time


app = wx.App(False)

PRESS_SCALER = 1 / 10

practice_clock = core.Clock()
testing_clock = core.Clock()
pre_practice_clock = core.Clock()

# constants with units in the visual degrees or degrees/loop
STARTING_POS = [-15, 0]
FINISH_LINE = 15
RING_PACE = (0.095, 0)

# constants with units in the seconds
COUNTDOWN_TIME = 3
FEEDBACK_TIME = 2.0
BREAK_TIME = 30.0
BLOCK_END_TIME = 30.0
PRACTICE_END_TIME = 5.0
MIN_SSD = 2
MAX_SSD = 4.9
HIT_BOX = [-1.20, 1.15]

INSTRUCTIONS_GO = (
    "Welcome to the task!\n\n" + "Please read the instructions for the task carefully.\n\n"
    + "On each trial, your job is to keep a dot inside of a moving ring by controlling its speed with your spacebar press.\n\n"
    + "Press the spacebar to move the dot across the screen.\n\n"
    + "The harder you press the spacebar, the faster the dot will move.\n\n"
    + "Please try your best to keep the dot within the ring. If you find the ball is going too fast, press the spacebar with less pressure  to reduce the dot’s speed.\n\n"
    + "For a brief period you will see a plus sign on the screen signifying that the trial is about to start and then the ring will begin to move from left to right. \n\n"
    + "As soon as the ring starts to move, you should press the spacebar to move the dot alongside it.\n\n"
    + "Try to keep the dot within the ring as it moves across the screen.\n\n"
    + "Let's practice moving the ball across the screen. When you are ready to begin, press enter."
)

INSTRUCTIONS_STOP = (
    "At some point while you move the dot across the screen, the screen will turn red.\n\n"
    + "When the screen turns red, this indicates that you should stop the movement of the dot by quickly stopping your spacebar press.\n\n"
    + "As you move the ball try to keep the space bar pressed the entire time and not let go of the space bar unless the screen turns red.\n\n"
    + "Let's have you practice stopping the dot as you move it across the screen.\n\nWhen you are ready to begin, press enter."
)

INSTRUCTIONS_PRACTICE = (
    "Great, now that you've practiced going and stopping let's put everything together and walk through the rest of the task.\n\n"
    + "The experiment is broken up into blocks, which are sets of trials. On certain blocks, you will be entirely responsible for controlling the dot and stopping its movement when the screen turns red. On other blocks there will be an artificial intelligence (AI) algorithm that will attempt to stop the dot when the screen turns red. On most trials it will succeed at stopping the dot irrespective of whether you stop pressing the spacebar, but sometimes it will fail.  When it fails to stop the dot, you are responsible for stopping the dot. Before each block, you will be told whether you are in a block that is AI-assisted or not. \n\n"
    + "The task is broken up into a practice phase where you will get feedback on your behavior and a testing phase which will not give you feedback.\n\n"
    + "When you are ready to begin the practice phase, press enter. \n\n")

INSTRUCTIONS_TESTING = (
    "We will now begin the testing phase. To summarize...\n\n"
    + "On each trial, your job is to keep a dot inside of a moving ring by controlling its speed.\n\n"
    +  "On certain blocks, you will be entirely responsible for controlling the dot and stopping its movement when the screen turns red. On other blocks there will be an artificial intelligence (AI) algorithm that will attempt to stop the dot when the screen turns red. On most trials it will succeed at stopping the dot irrespective of whether you stop pressing the spacebar, but sometimes it will fail.  When it fails to stop the dot, you are responsible for stopping the dot. Before each block, you will be told whether you are in a block that is AI-assisted or not.\n\n"
    + "Please try to keep the space bar pressed the entire time and not let go of the space bar unless the screen turns red. \n\n"
    + "When you are ready to begin the testing phase, press enter.")

END_TEXT = "Thank you for participating in this experiment!\n\nPlease press the spacebar to end this task."

NON_AI_TEXT = ("In this block the artificial intelligence algorithm is not engaged."
            + "\n\nYou are solely responsible for stopping the dots movement as quickly as possible when the screen turns red."
    + "\n\n Press enter to begin...")

AI_TEXT = ("In this block the artificial intelligence algorithm will be engaged. \n\n"
        + "On most trials, the AI algorithm will stop the dot irrespective of whether you stop pressing the spacebar, but sometimes it will fail."
        + "\n\nWhen it fails, you must stop the dot’s movement yourself." 
        + "\n\n Press Enter to begin...")

# feedback text options
PRESSURE_FEEDBACK = "Remember to keep the space pressed throughout the trial."
LATE_FEEDBACK = "You are starting too late...\n Press the space bar as soon as the ring starts moving."

NO_PRESS_TEXT = "Keep space bar pressed!"
LATE_TEXT = "You are starting too late!"

DEPRESS_FEEDBACK = "Remember to stop your pressing of the spacebar as soon as the background turns red."
HIT_FEEDBACK = "Please try to keep the dot within the circle as it moves across the screen."

def find_sequence(lst, target, sequence_length):
    count = 0
    for num in lst:
        if num == target:
            count += 1
            if count >= sequence_length:
                return True
        else:
            count = 0
    return False

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

    
def get_prob_dist_inputs(n_trials=200, block1=0, block2=0.8):
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
        
        block_labels = ['non-ai', 'ai']
        
    else:
        conditions = list(conditions_block2) + list(conditions_block1)
        
        block_labels = ['ai', 'non-ai']

    return conditions, block, block_labels


def setupPractice(num_stop=1, num_ai=1):
    practice_conditions = ["stop"] * num_stop + ["ai"] * num_ai
    np.random.shuffle(practice_conditions)

    return practice_conditions, len(practice_conditions)

def initStims():
    
    waitingForSpace = True
    Hit = False
    FinishLine = False
    stillMoving = True
    countdown = visual.TextStim(win=mywin, text="", height=1, pos=[0, 0])
    fixation = visual.TextStim(
        win=mywin, text="+", height=5, color=[255, 255, 255], pos=[0, 0]
    )
    
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
    
    return waitingForSpace, Hit, FinishLine, stillMoving, countdown, fixation, ring, ball, stopsignal, finishline


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
    conditions, block, block_labels = setup_trials()
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
    intro_stim_go = visual.TextStim(
        win=mywin, text=INSTRUCTIONS_GO, height=0.85, pos=[0, 0], wrapWidth=30
    )
    intro_stim_stop = visual.TextStim(
        win=mywin, text=INSTRUCTIONS_STOP, height=0.85, pos=[0, 0], wrapWidth=30
    )
    intro_stim_practice = visual.TextStim(
        win=mywin, text=INSTRUCTIONS_PRACTICE, height=0.85, pos=[0, 0], wrapWidth=30
    )
    intro_stim_testing = visual.TextStim(
        win=mywin, text=INSTRUCTIONS_TESTING, height=0.85, pos=[0, 0], wrapWidth=30
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
        win=mywin, text="Take a 10 second break, the block will resume shortly.", height=1.5, pos=[0, 3.5], wrapWidth=30
    )
    
    block_feedback = visual.TextStim(
        win=mywin,
        text="You have completed the first block of the experiment! \n Block 2 will start after a 30 second break. Please review your feedback if there is any...",
        height=1,
        pos=[0, 3.5],
        wrapWidth=30
    )
    
    ending_block_feedback = visual.TextStim(
        win=mywin,
        text="You have completed the second block of the experiment! \n Please review your feedback shown below if there is any...",
        height=1,
        pos=[0, 3.5],
        wrapWidth=30
    )
    
    AI_block_text = visual.TextStim(
        win=mywin,
        text=AI_TEXT,
        height=1,
        pos=[0, 0],
        wrapWidth=30
    )
    
    Non_AI_block_text = visual.TextStim(
        win=mywin,
        text=NON_AI_TEXT,
        height=1,
        pos=[0, 0],
        wrapWidth=30
    )  
    
    practice_end = visual.TextStim(
        win=mywin,
        text="Please review your feedback if there is any...",
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
    outside_circle_alert = visual.TextStim(
        win=mywin, text="keep the dot in the circle!", height=1, pos=[0, 5]
    )
    no_depress_alert = visual.TextStim(
        win=mywin, text="stop pressing when you see red!", height=1, pos=[0, 8]
    )
    practice_feedback_depress = visual.TextStim(
        win=mywin, text=DEPRESS_FEEDBACK, height=0.7, pos=[0, -4], wrapWidth=50
    )
    practice_feedback_hit = visual.TextStim(
        win=mywin, text=HIT_FEEDBACK, height=0.7, pos=[0, -6], wrapWidth=50
    )

    
    # INSTRUCTIONS
    pre_practice_clock.reset()
    intro_stim_go.draw()
    mywin.flip()
    waitingForSpace, Hit, FinishLine, stillMoving, countdown, fixation, ring, ball, stopsignal, finishline = initStims()
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_ENTER in scan_codes:
            waitingForSpace = False
    
    # Go Practice
    timer = core.CountdownTimer(COUNTDOWN_TIME)
    while timer.getTime() > 0:  # after 3s will become negative
        countdown.text = f"{timer.getTime():.0f}"
        ball.draw()
        ring.draw()
        if timer.getTime() < .5 and timer.getTime() > 0:
            fixation.draw()
        finishline.draw()
        mywin.flip()
    
    while not FinishLine:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        ring.pos += RING_PACE
        if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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
        finishline.draw()
        feedback.draw()
        mywin.flip()
    
    # Stop Practice
    intro_stim_stop.draw()
    mywin.flip()
    waitingForSpace, Hit, FinishLine, stillMoving, countdown, fixation, ring, ball, stopsignal, finishline = initStims()
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_ENTER in scan_codes:
            waitingForSpace = False
            
    timer = core.CountdownTimer(COUNTDOWN_TIME)
    while timer.getTime() > 0:  # after 3s will become negative
        countdown.text = f"{timer.getTime():.0f}"
        ball.draw()
        ring.draw()
        if timer.getTime() < .5 and timer.getTime() > 0:
            fixation.draw()
        finishline.draw()
        mywin.flip()
        
    SSD_timer = core.CountdownTimer(4)
    while SSD_timer.getTime() > 0:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        ring.pos += RING_PACE
        if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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

    # StopSignal
    end_trial_timer = core.CountdownTimer(1.5)
    while end_trial_timer.getTime() > 0:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
            not_moving_timer = core.CountdownTimer(1)
            ball.pos += (np.max(analog_codes) * PRESS_SCALER, 0)

        dist = ball.pos[0] - ring.pos[0] 
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
        mywin.flip()

    intro_stim_practice.draw()
    mywin.flip()
    waitingForSpace = True
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_ENTER in scan_codes:
            waitingForSpace = False
    
    pre_practice_duration = pre_practice_clock.getTime()
    
    # TRIAL LOOP
    # Practice Feedback Count
    feedback_tracker = []
    
    for count, trial in enumerate(trials):
        if count == 0:
            practice_clock.reset()

        if count == practice_len:
            feedback_tracker = []
            intro_stim_testing.draw()
            mywin.flip()
            waitingForSpace = True
            while waitingForSpace:
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                if HID_CODE_ENTER in scan_codes:
                    waitingForSpace = False
            

            testing_clock.reset()
            
            if block_labels[0] == 'ai':
                AI_block_text.draw()
                mywin.flip()
                time.sleep(1)
                waitingForSpace = True
                while waitingForSpace:
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    if HID_CODE_ENTER in scan_codes:
                        waitingForSpace = False
                        
            elif block_labels[0] == 'non-ai':
                Non_AI_block_text.draw()
                mywin.flip()
                time.sleep(1)
                waitingForSpace = True
                while waitingForSpace:
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    if HID_CODE_ENTER in scan_codes:
                        waitingForSpace = False
                        
            testing_clock.reset()

        if count == practice_len + (block / 2) or count == practice_len + (
            (block / 2) + block
        ):
            break_timer = core.CountdownTimer(BREAK_TIME)
            while break_timer.getTime() > 0:
                mywin.color = "grey"
                break_feedback.draw()
                mywin.flip()

        # Init Trial Data
        SSD = sample_SSD()
        trials.data.add("SSD", SSD)
        waitingForSpace, Hit, FinishLine, stillMoving, countdown, fixation, ring, ball, stopsignal, finishline = initStims()
        pressures = []
        distances = []
        timings = []

        # Countdown / ITI
        timer = core.CountdownTimer(COUNTDOWN_TIME)
        while timer.getTime() > 0:  # after 5s will become negative
            countdown.text = f"{timer.getTime():.0f}"
            ball.draw()
            ring.draw()
            if timer.getTime() < .5 and timer.getTime() > 0:
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
                if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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
                if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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

                if count < practice_len:
                    if find_sequence(pressures[25:-70], 0, 4):
                        no_pressure_alert.draw()
                    
                    if find_sequence(pressures[-60:],1, 3):
                        no_depress_alert.draw()
                        
                    if find_sequence(pressures[:25], 0, 8):
                        late_start_alert.draw()
                    
                    if distances[-1] < HIT_BOX[0]:
                        outside_circle_alert.draw()
                    elif distances[-1] > HIT_BOX[1]:
                        outside_circle_alert.draw()

                mywin.flip()

        elif trial["condition"] == "ai":
            trial_start = core.getTime()
            # SSD
            SSD_timer = core.CountdownTimer(SSD)
            while SSD_timer.getTime() > 0:
                scan_codes, analog_codes, _ = wp.read_full_buffer()
                timings.append(core.getTime() - trial_start)
                ring.pos += RING_PACE
                if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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
                if scan_codes and scan_codes[0] == HID_CODE_SPACE and analog_codes:
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

                if count < practice_len:
                    
                    if find_sequence(pressures[25:-70], 0, 4):
                        no_pressure_alert.draw()
                    
                    if find_sequence(pressures[-60:],1, 3):
                        no_depress_alert.draw()

                    if find_sequence(pressures[:25], 0, 8):
                        late_start_alert.draw()
                    
                    if distances[-1] < HIT_BOX[0]:
                        outside_circle_alert.draw()
                    elif distances[-1] > HIT_BOX[1]:
                        outside_circle_alert.draw()
                    
                mywin.flip()
                

        # Save Data
        trials.data.add("time_stamps", " ".join([str(elem) for elem in timings]))
        trials.data.add("pressures", " ".join([str(elem) for elem in pressures]))
        trials.data.add("distances", " ".join([str(elem) for elem in distances]))
        
        if count < practice_len:

            if find_sequence(pressures[25:-70], 0, 4):
                feedback_tracker.append("pressure")

            if find_sequence(pressures[-60:],1, 3):
                feedback_tracker.append("no_depress")

            if find_sequence(pressures[:25], 0, 8):
                feedback_tracker.append("late")

            if distances[-1] < HIT_BOX[0]:
                feedback_tracker.append("hit")
            elif distances[-1] > HIT_BOX[1]:
                feedback_tracker.append("hit")
        elif count >= practice_len:
            if find_sequence(pressures[25:-70], 0, 4):
                feedback_tracker.append("pressure")

            if find_sequence(pressures[-60:],1, 3):
                feedback_tracker.append("no_depress")

            if find_sequence(pressures[:25], 0, 8):
                feedback_tracker.append("late")

            if distances[-1] < HIT_BOX[0]:
                feedback_tracker.append("hit")
            elif distances[-1] > HIT_BOX[1]:
                feedback_tracker.append("hit")

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
            print(feedback_tracker)
            print(len(feedback_tracker))
            
            pressure_proportions = feedback_tracker.count("pressure") / (practice_len + block)
            late_proportions = feedback_tracker.count("late") / (practice_len + block)
            hit_proportions = feedback_tracker.count("hit") / (practice_len + block)
            no_depress_proportions = feedback_tracker.count("no_depress") / (practice_len + block)
            
            block_end_timer = core.CountdownTimer(BLOCK_END_TIME)
            while block_end_timer.getTime() > 0:
                mywin.color = "grey"
                block_feedback.draw()
                if late_proportions >= .25:
                    practice_feedback_late.draw()

                if pressure_proportions >= .25:
                    practice_feedback_pressure.draw()
                    
                if hit_proportions >= .25:
                    practice_feedback_hit.draw()
                    
                if no_depress_proportions >= .25:
                    practice_feedback_depress.draw()
                mywin.flip()
            
            if block_labels[1] == 'ai':
                AI_block_text.draw()
                mywin.flip()
                waitingForSpace = True
                while waitingForSpace:
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    if HID_CODE_ENTER in scan_codes:
                        waitingForSpace = False
                        
            elif block_labels[1] == 'non-ai':
                Non_AI_block_text.draw()
                mywin.flip()
                waitingForSpace = True
                while waitingForSpace:
                    scan_codes, analog_codes, _ = wp.read_full_buffer()
                    if HID_CODE_ENTER in scan_codes:
                        waitingForSpace = False
            
            #reseting feedback
            feedback_tracker = []
                        
        elif count + 1 == practice_len:
            print(feedback_tracker)
            print(len(feedback_tracker))
            practice_end_timer = core.CountdownTimer(PRACTICE_END_TIME)
            practice_duration = practice_clock.getTime()
            
            pressure_proportions = feedback_tracker.count("pressure") / practice_len
            late_proportions = feedback_tracker.count("late") / practice_len
            hit_proportions = feedback_tracker.count("hit") / practice_len
            no_depress_proportions = feedback_tracker.count("no_depress") / practice_len

            while practice_end_timer.getTime() > 0:
                mywin.color = "grey"
                practice_end.draw()
                if late_proportions >= .25:
                    practice_feedback_late.draw()

                if pressure_proportions >= .25:
                    practice_feedback_pressure.draw()
                    
                if hit_proportions >= .25:
                    practice_feedback_hit.draw()
                    
                if no_depress_proportions >= .25:
                    practice_feedback_depress.draw()

                mywin.flip()
    # FINISH
    
    pressure_proportions = feedback_tracker.count("pressure") / (practice_len + block)
    late_proportions = feedback_tracker.count("late") / (practice_len + block)
    hit_proportions = feedback_tracker.count("hit") / (practice_len + block)
    no_depress_proportions = feedback_tracker.count("no_depress") / (practice_len + block)
    
    block_end_timer = core.CountdownTimer(BLOCK_END_TIME)
    while block_end_timer.getTime() > 0:
        mywin.color = "grey"
        ending_block_feedback.draw()
        if late_proportions >= .25:
            practice_feedback_late.draw()

        if pressure_proportions >= .25:
            practice_feedback_pressure.draw()

        if hit_proportions >= .25:
            practice_feedback_hit.draw()

        if no_depress_proportions >= .25:
            practice_feedback_depress.draw()
        mywin.flip()
    
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
    print(f"pre-Practice pahse duration: {pre_practice_duration} seconds")

    # Cleanup
    mywin.close()
    core.quit()
