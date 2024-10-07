##################################
# Importing  #####################
##################################

from psychopy import core, visual, sound, event
import random as rd
import decimal
import sys
import numpy as np  
import os
import copy as cp
import localLib


##############################
# Setup  #####################
##############################

target_val = [-.03,-.03,-.03]

win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[0,0,0],
                  fullscr = True,
                  allowGUI=False)
fps=round(win.getActualFrameRate())
win.close()

if fps!=60:
    print()
    print("WARNING....  Frame Rate is not 60hz.")
    input("Enter to Continue, control-c to quit.  ") 

run_mode = False
if run_mode == False:
    nt_inst_t = 5
    nt_rest_tasks = 5
    nt_train = 2
else:
    nt_inst_t = 50
    nt_rest_tasks = 32
    nt_train = 10
[fptr,sub]=localLib.startExp(expName="sb2",runMode=run_mode,fps=fps)


    
    
    
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
seed = rd.randrange(1e6)
rng = rd.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)

header=['sub','task','cond1','cond2','rt','inputResp','training','accuracy','trial','block','2fast']


########################################
# Functions  #####################
########################################


### Logestics:

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


def getResp(truth, abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    if truth == True:
        acc = int(resp=='m')
    else:
        acc = int(resp=="x")
    return([resp,rt,acc])

def feedback(resp,correctResp):
    if (resp==correctResp):
        correct1.play()
        core.wait(.1)
        correct2.play()
    else:
        error.play()
    return(resp==correctResp)

### Conjuction Search:

def conjunct(truth, size, set_size, st, ins = False):
    if size == set_size[1]:
        x = np.arange(-120,121,60)
        y = np.arange(-120,121,60)
    else:
        x = np.arange(-90,90,60)
        y = np.arange(-90,90,60)

    xx, yy = np.meshgrid(x,y)
    grid = np.stack((xx,yy), axis = -1)
    grid_flat = [i2 for i in grid for i2 in i]
    grid_select = rd.sample(grid_flat, size)
    jitter = np.random.uniform(low=-20, high=20, size=(len(grid_select),2))
    grid_jitter = grid_select + jitter
    stims = []
    for pos in range(size):
        x,y = grid_jitter[pos]
        text_stim = visual.TextStim(
            win = win,
            text = st,
            pos = (x, y),
            color = 'white',
            height = 20
        )
        stims.append(text_stim)
    if truth == True:
        pick = rd.sample(range(size), 1)
        x,y = grid_jitter[pick[0]]
        text_stim = visual.TextStim(
            win = win,
            text = st,
            pos = (x, y),
            color = 'white',
            height = 20,
            flipHoriz = True
        )
        stims[pick[0]] = text_stim
        if ins == True:
            text_stim2 = visual.TextStim(
                win = win,
                text = st,
                pos = (x, y),
                color = 'red',
                height = 20,
                flipHoriz = True
            )
            stims[pick[0]] = text_stim2
    return(stims)


def conjunctTrial(size, truth, set_size, st):
    x = visual.TextStim(
        win = win,
        text = "X: NO backward N",
        pos = (-400,-475),
        color = "white"
    )
    m = visual.TextStim(
        win = win,
        text = "M: YES backward N",
        pos = (400,-475),
        color = "white"
    )
    frameTimes=[30,30,1]  #at 60hz
    stims = conjunct(truth, size, set_size, st)
    frame=[]
    tstim = [visual.TextStim(win,"+"), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = [visual.TextStim(win,""), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = stims+[x,m]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    if rt < .2:
        warn()
        tooFast = 1
    else:
        tooFast = 0

    return(resp,rt,acc,tooFast)



def runConjunct(trial_size, set_size = [2,18], method = 1, train = False, rnd=1):
    st = "N" if train == False else "N"
    truth = []
    size = []
    if method == 1:
        for i in range(trial_size):
            truth.append(i%2)
            size.append(set_size[i%2])
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            truth.append(x[0]%2)
            size.append(set_size[x[1]%2])
    rd.shuffle(truth)
    rd.shuffle(size)
    for i in range(trial_size):
        [resp,rt,acc,tooFast] = conjunctTrial(size[i],truth[i],set_size,st)

        cond = 0 if size[i] == set_size[0]  else 1
        resp2 = 1 if resp == "m" else 0
        out=[sub,2,cond,truth[i],round(rt,2),resp2,int(train),int(acc),i+1,rnd,tooFast]
        print(*out,sep=", ",file=fptr)
        fptr.flush()



runConjunct(10, set_size = [2,18], method = 1, train = True)
