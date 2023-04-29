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

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `stimGlob` INT(3) UNSIGNED NOT NULL,"
    "  `stimLoc` INT(1) UNSIGNED NOT NULL,"
    "  `correctResp` CHAR(1),"
    "  `resp` CHAR(1),"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `stimGlob`, `StimLoc`, `correctResp`,`resp`,`rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

if useDB:
    sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
    
    
########################################
# GLOBAL SETTINGS  #####################
########################################
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

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)

########################################
# Functions  #####################
########################################







def runFrames(frame,frameTimes,timerStart=3):
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


def getResp(in_the_set, abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    if in_the_set == True:
        resp = int(resp=='m')
    else:
        resp = int(resp=="x")
    return([resp,rt])

def feedback(resp,correctResp):
    if (resp==correctResp):
        correct1.play()
        core.wait(.1)
        correct2.play()
    else:
        error.play()
    return(resp==correctResp)



def conjunct(truth, size):
    radius = 100
    num_points = int(np.sqrt(size)+2)
    ang = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    radi = np.linspace(0, radius,num_points)
    radi*= 2.5
    rr, aa = np.meshgrid(radi,ang)

    x = rr*np.cos(aa)
    y = rr*np.sin(aa)
    grid = np.stack((x,y), axis = -1)
    grid_flat = [i2 for i in grid for i2 in i]
    grid_select = random.sample(grid_flat, size)
    print(grid_select)
    jitter = np.random.uniform(low=-15, high=15, size=(len(grid_select),2))
    grid_jitter = grid_select + jitter
    stims = []
    for pos in range(size):
        x,y = grid_jitter[pos]
        print(f"pos:{pos}, x:{x} ,y:{y}")
        text_stim = visual.TextStim(
            win = win,
            text = 'N',
            pos = (x, y),
            color = 'white',
            height = 20
        )
        stims.append(text_stim)
    if truth == True:
        pick = random.sample(range(size), 1)
        x,y = grid_jitter[pick[0]]
        text_stim = visual.TextStim(
            win = win,
            text = 'N',
            pos = (x, y),
            color = 'green',
            height = 20,
            flipHoriz = True
        )
        stims[pick[0]] = text_stim
    return(stims)


def trial(set_size, truth):
    frameTimes=[60,1]  #at 60hz
    stims = conjunct(truth, set_size)
    print(len(stims))
    frame=[]
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes)
    [resp,rt]=getResp(in_the_set = truth)
    acc=feedback(resp,1)
    # print(rt, resp)
    return(resp)


truth = []
size = []
for i in range(20):
    truth.append(i%2)
    size.append(6+6*(i%2)*5)

random.shuffle(truth)
random.shuffle(size)

for i in range(20):
    trial(size[i],truth[i])


hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)


core.quit()
