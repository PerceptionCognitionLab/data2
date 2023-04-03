from psychopy import core, visual, sound, event
import random as rd
import decimal
import sys
import numpy as np  
import os
import copy as cp
from funs import *





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



def conjunct(truth, size, set_size):
    if size == set_size[1]:
        x = np.arange(-100,101,60)
        y = np.arange(-100,101,60)
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
        pick = rd.sample(range(size), 1)
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


def conjunctTrial(size, truth, set_size):
    frameTimes=[60,1]  #at 60hz
    stims = conjunct(truth, size, set_size)
    frame=[]
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes)
    [resp,rt]=getResp(in_the_set = truth)
    acc=feedback(resp,1)
    # print(rt, resp)
    return(resp)


def runConjunct(trial_size, set_size = [4,12], method = 1):
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
    print(size)
    rd.shuffle(truth)
    rd.shuffle(size)
    for i in range(20):
        conjunctTrial(size[i],truth[i],set_size)


