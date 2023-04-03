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


##############################
# Setup  #####################
##############################

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
seed = rd.randrange(1e6)
rng = rd.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)


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



### Conjuction Search:

def conjunct(truth, size, set_size, st):
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
    return(stims)


def conjunctTrial(size, truth, set_size, st):
    frameTimes=[60,1]  #at 60hz
    stims = conjunct(truth, size, set_size, st)
    frame=[]
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes)
    [resp,rt]=getResp(truth = truth)
    acc=feedback(resp,1)
    return(resp)


def runConjunct(trial_size, set_size = [4,12], method = 1, trian = False):
    st = "N" if trian == False else "L"
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
    for i in range(20):
        conjunctTrial(size[i],truth[i],set_size,st)


### Mental Rotation:


rect = visual.Rect(
	win = win, 
	units = "pix",
	width = 40,
	height = 40, 
	lineColor = [0, 0, 0]
)


def curveLine(ang, dir = 0):
    center = (0, 100)
    if ang == 180:
        center = (100, 0)
    radius = 100
    start_angle = 0
    end_angle =  ang
    num_points = 10000
    angles = [np.deg2rad(angle) for angle in np.linspace(start_angle, end_angle, num_points)]

    x_coords = center[0] + radius * np.cos(angles)
    y_coords = center[1] + radius * np.sin(angles)
    coords = [(x,y) for x,y in zip(x_coords, y_coords)]
    txt = f'Rotate {ang}\u00B0 clockwise!'
    if dir == 3:
        coords = [(-x,y) for x,y in zip(x_coords, y_coords)]
        txt = f'Rotate {ang}\u00B0 counter clockwise!'
    if ang != 0:
        if ang == 180:
            coords = np.flip(coords, axis=1)
            [x,y] = coords[-1]
            pointer1_vert1 = [(x,y), (x+10,y+12)]
            pointer1_vert2 = [(x,y), (x+10,y-10)]
        else:
            [x,y] = coords[0]
            pointer1_vert1 = [(x,y), (x+10,y+10)]
            pointer1_vert2 = [(x,y), (x-12,y+10)]      
        wedge = visual.ShapeStim(
            win=win, 
            lineColor='white', 
            vertices=coords,
            closeShape=False)
        line1 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=pointer1_vert1
        )
        line2 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=pointer1_vert2
        )
        text_stim = visual.TextStim(
            win = win,
            text = txt,
            pos = (0,250),
            color = 'white'
        )
        return(wedge,line1,line2,text_stim)
    else:
        text_stim = visual.TextStim(
            win = win,
            text = f'Do not rotate! \n Are the two grids the same?',
            pos = (0,250),
            color = 'white'
        )
        return(text_stim)



def rotMat(orig_mat, rotation, flip = False):
    rot_mat = orig_mat
    for r in range(rotation):
        rot_mat = np.rot90(rot_mat)
    if flip == True:
        ax = rd.choice([0,1])
        if rotation == 2: 
            rot_mat = np.flip(rot_mat, axis = ax)
        else:
            rot_mat = np.flip(rot_mat, axis = ax)
    return rot_mat 			


def presMat(orig_mat, rot_mat):
	rect = visual.Rect(
		win = win, 
		units = "pix",
		width = 60,
		height = 60, 
		lineColor = [0, 0, 0]
	)
	stims = []
	y = -100 		
	for row in range(3):
		x1 = -400
		x2 = 400
		for col in range(3):
			trect = cp.copy(rect)
			if orig_mat[row,col] == 1:
				trect.fillColor = [1,-1,-1]
			else:
				trect.fillColor = [-1,-1,1]
			trect.pos = [x1,y]
			stims.append(trect)
			trect2 = cp.copy(rect)
			x1+=60
			if rot_mat[row,col] == 1:
				trect2.fillColor = [1,-1,-1]
			else:
				trect2.fillColor = [-1,-1,1]
			trect2.pos = [x2,y]
			stims.append(trect2)
			x2+=60
		y+=60
	return(stims)


def menRotTrial(stims, truth):
    frameTimes=[30,30,1]  #at 60hz
    frame=[]
    #frame.append(visual.BufferImageStim(win, stim = stims))
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.TextStim(win,""))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes)
    [resp,rt]=getResp(truth = truth)
    acc=feedback(resp,1)
    print(truth,resp)



def runMenRot(trial_size, method = 1, rotations = [0,1], train = False):
    mats = []
    if train == True:
        mats.append(np.array([[1,0,0],[1,0,0],[0,0,0]]))
        mats.append(np.array([[0,0,0],[0,1,0],[0,1,1]]))
        mats.append(np.array([[1,1,0],[0,1,1],[0,0,0]]))
        mats.append(np.array([[1,0,0],[0,0,0],[0,1,0]]))
    else:
        mats.append(np.array([[0,0,0],[1,1,0],[1,0,1]]))
        mats.append(np.array([[0,0,1],[1,0,0],[1,0,1]]))
        mats.append(np.array([[0,1,0],[1,0,1],[1,0,0]]))
        mats.append(np.array([[0,1,0],[1,0,0],[1,0,1]]))
        mats.append(np.array([[1,0,0],[0,0,0],[0,1,1]]))
        mats.append(np.array([[0,1,0],[1,0,1],[0,0,0]]))

    rots = []
    order = []
    if method == 1:
        for i in range(trial_size):
            order.append(i%2)
            rots.append(rotations[i%2])
    print(rots)
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            order.append(x[0]%2)
            rots.append(rotations[x[1]%2])
    rd.shuffle(order)
    rd.shuffle(rots)
    for t in range(trial_size):
        if rots[t] == 1:
            x = rd.choice([1,3])
        else:
            x = rots[t]
        if order[t] == 1:
            tmat = rd.sample(mats,k=1)
            tmats = [tmat[0],rotMat(tmat[0],x)]
        else:
            tmat = rd.sample(mats,k=1)
            tmats = [tmat[0],rotMat(tmat[0],x,flip=True)]
        stim = presMat(tmats[0], tmats[1])    
        if rots[t] != 0:
            if rots[t] == 1:
                [wedge90,line1,line2,txt] = curveLine(90, dir = x)
            elif rots[t] == 2:
                [wedge90,line1,line2,txt] = curveLine(180)
            stim.append(wedge90)
            stim.append(line1)
            stim.append(line2)
            stim.append(txt)
        else:
            txt = curveLine(0)
            stim.append(txt)
        menRotTrial(stim, order[t])


### Memory span:
def runMemSpan(trial_size, target_size=[2,5], method = 1, train = False):
    target = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    if train == True: 
        target = []
        for i in range(10): target.append(str(i))
    order = []
    size = []
    if method == 1:
        for i in range(trial_size):
            order.append(i%2)
            size.append(target_size[i%2])
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            order.append(x[0]%2)
            size.append(target_size[x[1]%2])
    rd.shuffle(order)
    rd.shuffle(size)
    print(order)
    for t in range(trial_size):
        print(f"target_{t}={target}")
        letters = target
        print(f"letters_{t}={letters}")
        q = rd.sample(letters, k = size[t])
        if order[t] == True:
            print(f"one")
            s = rd.choice(q)
            truth = True
        else:
            print(f"two")
            wrong_s = []
            for i in range(len(letters)):
                if letters[i] not in q: 
                    wrong_s.append(letters[i])
            s = rd.choice(wrong_s)
            truth = False
        q = " ".join(q)
        q_stim = visual.TextStim(
            win = win,
            text = q,
            pos = (0,0),
            color = 'white'
        )
        s_stim = visual.TextStim(
            win = win,
            text = s,
            pos = (0,0),
            color = 'white'
        )
        s_stim.size = q_stim.size = 5
        memSpanTrial(truth, q_stim, s_stim)


def mask():
    mask1 = visual.TextStim(
        win = win,
        text = "@",
        pos = (0,0),
        color = 'white'
    )
    mask2 = visual.TextStim(
        win = win,
        text = "#",
        pos = (0,0),
        color = 'white'
    )
    return(mask1, mask2)

def memSpanTrial(truth, q, s):
    frameTimes=[60,30,60,30,30,1]  #at 60hz
    frame=[]
    [mask1,mask2] = mask()
    frame.append(visual.TextStim(win,"+"))
    frame.append(q)
    frame.append(visual.TextStim(win,""))
    frame.append(s)
    frame.append(mask1)
    frame.append(mask2)

    runFrames(frame,frameTimes)
    [resp,rt]=getResp(truth = truth)
    acc=feedback(resp,1)
    print(rt, resp)

### Inspection time:






def getRespInsTime(s, abortKey='9'):
    letters = ["a","s","d","f","g","h","j","k","l",abortKey]
    keys=event.getKeys(keyList=letters,timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=letters,timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    resp = int(resp==s)
    return([resp,rt])



def insTimeTrial(t, q, s):
    frameTimes=[60,t,30,30,1]  #at 60hz
    frame=[]
    [mask1,mask2] = mask()
    frame.append(visual.TextStim(win,"+"))
    frame.append(q)
    frame.append(mask1)
    frame.append(mask2)
    frame.append(visual.TextStim(win,"Enter the letter you just saw:"))
    runFrames(frame,frameTimes)
    [resp,rt]=getRespInsTime(s)
    acc=feedback(resp,1)
    print(rt, resp)
    return(resp)




def runInsTime(trial_size):
    letters = ["a","s","d","f","g","h","j","k","l"]

    counter = 0
    t = 50
    for i in range(trial_size):
        x = rd.choice(letters)
        q_stim = visual.TextStim(
            win = win,
            text = x,
            pos = (0,0),
            color = 'white'
        )
        z = insTimeTrial(t, q_stim, x)
        counter += z
        if z == 0:
            t += 5
            counter = 0
        if counter == 2:
            t -=5
            counter = 0
        print(f"count: {t}")




# runInsTime(10)
# runMemSpan(10, target_size=[2,5], method = 1, train = False)
runMenRot(20, method = 1, rotations = [0,1], train = False)
# runConjunct(10, set_size = [4,12], method = 1, trian = False)


hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

print(hz)
core.quit()

