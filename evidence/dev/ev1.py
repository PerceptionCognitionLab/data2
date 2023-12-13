from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os


##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = exp
expName='test'
abortKey='q'



if useDB:
    sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
    
scale=400

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)





def targetLetters(size):
	letters = ["Hello"] * size
	x = random.choices(letters, k = size)
	return(x)
	

def runFrames(frame, frameTimes, wait_for_key=True):
    event.clearEvents()
    currentFrame = 0
    frame_count = len(frame)
    
    while currentFrame < frame_count:
        frame[currentFrame].draw()
        win.flip()

        keys = event.getKeys()
        if keys:
            currentFrame += 1

        event.clearEvents()

    if wait_for_key:
        event.waitKeys()


def getResp():
    keys = event.waitKeys()

    resp = keys[0]  # Get the first key pressed
    rt = timer.getTime()  # Use the timer to get the response time

    print(f"Key pressed: {resp}, Response time: {rt}")
    return [resp, rt]

def trial(set_size):
    frameTimes = [60, 30, 60, 1]  # at 60hz
    target_list = targetLetters(set_size)
    q = "Hello"  
    
    
    hello_frame = visual.TextStim(win, "Hello")

    key_press_counter = 0

    while key_press_counter < 10:  
        frame = [
            visual.TextStim(win, "+"),
            visual.TextStim(win, " ".join(target_list)),
            visual.TextStim(win, ""),
            visual.TextStim(win, q),
            visual.TextStim(win, ""),
            visual.TextStim(win, q),
            visual.TextStim(win, ""),
            visual.TextStim(win, q),
            visual.TextStim(win, q),
            visual.TextStim(win, q)
        ]

        runFrames(frame, frameTimes)
        resp,rt = getResp()
        print(f"Key pressed: {resp}, Response time: {rt}")
        key_press_counter += 1

        hello_frame.draw()
        win.flip()
        event.waitKeys()  
    

x = [5,5,5,5,5,5,5]

for i in x:
	trial(i)

hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)


core.quit()
