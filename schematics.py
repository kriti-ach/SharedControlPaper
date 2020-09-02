from psychopy import visual, core, event #import some libraries from PsychoPy
from wooting_utils import WootingPython, HID_CODE_SPACE
import numpy as np
import sys

WIN_SIZE = [1000,600]
STARTING_POS = [-9,0]

DIRECTION = 1
RING_PACE = (0.065, 0)

SSD = 1.500



if __name__ == "__main__":
    print('setting up kb')
    wp = WootingPython()

    wp.initialise()
    wp.is_initialised()
    wp.get_info()
    print('> Checking if keyboard is connected...')
    print(wp.is_connected())
    if not wp.is_connected():
        print('> ERROR: No keyboard found! Connect it and try again.')
        sys.exit(-1)
        
    wp.get_info()

    #create a window
    mywin = visual.Window(WIN_SIZE, monitor="testMonitor", units="deg", fullscr=False)

    #create some stimuli
    # fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)
    ring = visual.Circle(win=mywin, radius=2, edges=32, pos=STARTING_POS,  lineWidth=15, lineColor='white')
    ball = visual.Circle(win=mywin, radius=.8, edges=32, pos=STARTING_POS,  lineWidth=10, lineColor='white', fillColor='white')
    

    
    # COUNTDOWN / ITI
    # countdown = visual.TextStim(win=mywin, text='3', height=1.5, pos=[0,3])
    # waitingForSpace = True
    # while waitingForSpace:
    #     ball.draw()
    #     ring.draw()
    #     countdown.draw()
    #     mywin.flip()
    #     scan_codes, analog_codes, _ = wp.read_full_buffer()
    #     if HID_CODE_SPACE in scan_codes:
    #         waitingForSpace = False    

 
    # SSD
    # ring.pos += (1.2, 0)
    # ball.pos += (1.4, 0)
    # waitingForSpace = True
    # while waitingForSpace:
    #     scan_codes, analog_codes, _ = wp.read_full_buffer()
    #     if HID_CODE_SPACE in scan_codes:
    #         waitingForSpace = False    
    #     # fixation.draw()
    #     ball.draw()
    #     ring.draw()
    #     mywin.flip()

    # Stop Signal
    # ring.pos += (1.5, 0)
    # ball.pos += (1.7, 0)
    # stopsignal = visual.Rect(win=mywin, width=28, height=17, pos=(0,0),  lineWidth=50, lineColor='white')
    # waitingForSpace = True
    # while waitingForSpace:
    #     scan_codes, analog_codes, _ = wp.read_full_buffer()
    #     if HID_CODE_SPACE in scan_codes:
    #         waitingForSpace = False    
    #     # fixation.draw()
    #     ball.draw()
    #     ring.draw()
    #     stopsignal.draw()
    #     mywin.flip()

    # Stop Success
    # ring.pos += (1.5, 0)
    # ball.pos += (1.8, 0)
    # stopsignal = visual.Rect(win=mywin, width=28, height=17, pos=(0,0),  lineWidth=50, lineColor='white')
    # feedback = visual.TextStim(win=mywin, text='Good Job', height=1, pos=[0,2.5])
    # waitingForSpace = True
    # while waitingForSpace:
    #     scan_codes, analog_codes, _ = wp.read_full_buffer()
    #     if HID_CODE_SPACE in scan_codes:
    #         waitingForSpace = False    
    #     # fixation.draw()
    #     ball.draw()
    #     ring.draw()
    #     stopsignal.draw()
    #     feedback.draw()
    #     mywin.flip()

    # Stop Fail
    ring.pos += (1.5, 0)
    ball.pos += (2.6, 0)
    stopsignal = visual.Rect(win=mywin, width=28, height=17, pos=(0,0),  lineWidth=50, lineColor='Black')
    feedback = visual.TextStim(win=mywin, text='Please Try Harder to Brake', height=1, pos=[0,2.5])
    waitingForSpace = True
    while waitingForSpace:
        scan_codes, analog_codes, _ = wp.read_full_buffer()
        if HID_CODE_SPACE in scan_codes:
            waitingForSpace = False    
        # fixation.draw()
        ball.draw()
        ring.draw()
        stopsignal.draw()
        feedback.draw()
        mywin.flip()



    #cleanup
    mywin.close()
    core.quit()