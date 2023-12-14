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


def runFrames(frame,frameTimes,timerStart=1):
    event.clearEvents()
    currentFrame=0
    cumTimes=np.cumsum(frameTimes)    
    for refresh in range(max(cumTimes)):
        if refresh in cumTimes:
            currentFrame=currentFrame+1
            if currentFrame==timerStart:
                timer.reset()
        frame[currentFrame].draw()
        win.flip()  

	

def getResp(abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   

    return([resp,rt])


message=visual.TextStim(win,text="m",
		        pos=(0,0),
		        height=20)
messagex=visual.TextStim(win,text="x",
		        pos=(0,0),
		        height=20)

c=visual.TextStim(win,text="+",
		        pos=(0,0),
		        height=20)


frame=[c,message,messagex]
random.shuffle(frame)
frameTimes=[60,60]
all_resp=[]
for i in range(5):
	
	runFrames(frame,frameTimes)
	response = getResp()
	all_resp.append(response)

hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

for i in range(5):
	print(all_resp[i])
core.quit()
