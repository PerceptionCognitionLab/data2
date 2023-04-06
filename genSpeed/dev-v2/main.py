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

[fptr,sub]=localLib.startExp(expName="genSpeed",runMode=False,fps=fps)


    
    
    
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

header=['sub','task','cond','cor','rt','resp','block','acc','trial']


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
    frameTimes=[30,30,1]  #at 60hz
    stims = conjunct(truth, size, set_size, st)
    frame=[]
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.TextStim(win,""))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    return(resp,rt,acc)


def runConjunct(trial_size, set_size = [4,12], method = 1, train = False):
    st = "N" if train == False else "L"
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
        [resp,rt,acc] = conjunctTrial(size[i],truth[i],set_size,st)

        cond = 0 if size[i] == 4 else 1
        resp2 = 1 if resp == "m" else 0
        out=[sub,2,cond,truth[i],rt,resp2,int(train),int(acc),i+1]
        print(*out,sep=", ",file=fptr)
        fptr.flush()




### Mental Rotation:



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
		x1 = -300
		x2 = 200; print(f"rot_mat:{orig_mat}")
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
    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    return(resp, rt, acc)



def runMenRot(trial_size, method = 1, rotations = [0,1,3], train = False):
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
    
    for i in range(len(mats)):
        temp_mat = np.flip(mats[i], axis = 1)
        mats.append(temp_mat)
    order = []
    stim_grid = []
    for i in range(len(mats)): 
        stim_grid.append([i,rotations[0]])
        stim_grid.append([i,rotations[1]])
        stim_grid.append([i,rotations[2]])
    if method == 1:
        for i in range(trial_size):
            order.append(i%2)
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            order.append(x[0])

    rd.shuffle(stim_grid)
    rd.shuffle(order)
    for t in range(trial_size):
        x = stim_grid[t][1]
        print(f"stim:{stim_grid[t]}")
        print(f"truth:{order[t]}")
        print(f"mat:{mats[stim_grid[t][0]]}")
        print(x)
        if order[t] == 1:
            tmat_t = mats[stim_grid[t][0]]
            tmat_q = rotMat(tmat_t,x)
        else:
            tmat_t = rd.choice(mats)
            tmat_q = rotMat(tmat_t,x,flip=True)
        print(f"t:{tmat_t}")
        print(f"q:{tmat_q}")
        stims = presMat(tmat_t, tmat_q)    
        if x != 0:
            if x in [1,3]:
                [wedge90,line1,line2,txt] = curveLine(90, dir = x)
            elif x == 2:
                [wedge90,line1,line2,txt] = curveLine(180)
            stims.append(wedge90)
            stims.append(line1)
            stims.append(line2)
            stims.append(txt)
        else:
            txt = curveLine(0)
            stims.append(txt)
        [resp,rt,acc] = menRotTrial(stims, order[t])
        
        if x == 0:
            cond = 0
        else:
            cond = 1 if x == 1 else -1 
        resp2 = 1 if resp == "m" else 0
        out=[sub,1,cond,order[t],rt,resp2,int(train),int(acc),t+1]
        print(*out,sep=", ",file=fptr)
        fptr.flush()




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
        [resp,rt,acc] = memSpanTrial(truth, q_stim, s_stim)

        cond = 0 if size[t] == 2 else 1 
        resp2 = 1 if resp == "m" else 0
        out=[sub,3,cond,order[t],rt,resp2,int(train),int(acc),t+1]
        print(*out,sep=", ",file=fptr)
        fptr.flush()



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
    frameTimes=[60,30,60,1]  #at 60hz
    frame=[]
    [mask1,mask2] = mask()
    frame.append(visual.TextStim(win,"+"))
    frame.append(q)
    frame.append(visual.TextStim(win,""))
    frame.append(s)
    # frame.append(mask1)
    # frame.append(mask2)

    runFrames(frame,frameTimes,timerStart=1)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    return(resp,rt,acc)

### Inspection time:




def getRespInsTime(s, abortKey='9'):
    letters = ["a","s","d","f","g","h","j","k","l",abortKey]
    keys=event.getKeys(keyList=letters,timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=letters,timeStamped=timer)
    resp=keys[0][0]
    resp=resp.upper()
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    return([resp,rt])



def insTimeTrial(t, q, s):
    frameTimes=[30,30,t,3,3,1]  #at 60hz
    frame=[]
    [mask1,mask2] = mask()
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.TextStim(win,""))
    frame.append(q)
    frame.append(mask1)
    frame.append(mask2)
    frame.append(visual.TextStim(win,""))
    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt]=getRespInsTime(s)
    resp2 = int(resp==s)
    acc=feedback(resp2,1)
    print(rt, resp)
    return(resp,rt,acc)




def runInsTime(trial_size):
    letters = ["A","S","D","F","G","H","J","K","L"]
    counter = 0
    t = 8
    for i in range(trial_size):
        x = rd.choice(letters)
        x.upper()
        q_stim = visual.TextStim(
            win = win,
            text = x,
            pos = (0,0),
            color = 'white'
        )
        if i < 4:
            [resp,rt,acc] = insTimeTrial(20, q_stim, x)
        else:
            [resp,rt,acc] = insTimeTrial(t, q_stim, x)
            counter += acc
            if counter == 0:
                t += 1
                counter = 0
            if counter == 2:
                t -= 1
                counter = 0
        out=[sub,0,t,x,rt,resp,"NA",int(acc),i+1]
        print(*out,sep=", ",file=fptr)
        fptr.flush()

### Buffer:

def getRespBuffer(abortKey='9'):
    keys=event.getKeys(keyList=["s",abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=("s",abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    return("confirmed")




def expBuffer():
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Well done on your training! \nPress enter when ready..."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    txt = "Now let's begin. \nPress enter when ready... "
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,txt))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()

def trainBuffer(exp):
    if exp == 1:
        txt = "Welcome to the Mental Rotation Task. Your objective is to determine whether a presented grid needs to be rotated or not. \nIf the grid matches the original grid, please enter 'M'. If it does not match, please enter 'X'. \nIf you have any questions, please call the RA over. \nPress 'S' to begin the task."
    elif exp == 2:
        txt = "Welcome to the Conjunction Search Task. Your objective is to identify whether there is a backward letter in the list of letters presented. \nPlease press 'M' if there is a backward letter, and 'X' if there is not. \nIf you have any questions, please call the RA over. \nPress 'S' to begin the task."
    elif exp == 3:
        txt = "Welcome to the Memory Scan Task. \nIn this task, you will be presented with a list of letters or digits, followed by a single item. Your objective is to determine whether the subsequent item was in the original list. \nPlease press 'M' if the subsequent item was in the original list, and 'X' if it was not. \nIf you have any questions, please call the RA over. \nPress 'S' to begin the task."

    frameTimes=[30,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Welcome to the next task! \nTake your time, and if you have any questions, please do not hesitate to ask. \nPlease press 'S' to begin."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    frameTimes=[30,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,txt))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    frameTimes=[30,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Now let's do a training round, \nPlease press 'S' to begin."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()

def intialBuffer():
    frameTimes=[30,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Welcome! \nPress press 'S' when ready..."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    txt = "Welcome to the Inspection Time Task. \nIn this task, a letter will be presented to you, followed by a mask. \nYour objective is to identify the letter that was presented. \nPlease enter the corresponding letter on the keyboard. \nIf you have any questions, please don't hesitate to ask the RA. \nPress 'S' to begin the task. "
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,txt))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()


def expBuffer():
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Well done on completing the training round! \nPlease press 'S' to begin the next task."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    txt = "Great! Let's begin. \nRemember to stay focused and do your best. \nPlease press 'S' to start the task."
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,txt))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()





print(*header,sep=", ",file=fptr)
fptr.flush()


# intialBuffer()
# runInsTime(5)
# trainBuffer(1)
# runMenRot(5, method = 1, rotations = [0,1,3], train = False)
# expBuffer()
# runMenRot(5, method = 1, rotations = [0,1,3], train = True)
# trainBuffer(2)
runConjunct(5, set_size = [4,12], method = 1, train = False)
expBuffer()
runConjunct(5, set_size = [4,12], method = 1, train = True)
trainBuffer(3)
runMemSpan(5, target_size=[2,5], method = 1, train = False)
expBuffer()
runMemSpan(5, target_size=[2,5], method = 1, train = True)

# runInsTime(50)
# runMenRot(20, method = 1, rotations = [0,1,3], train = False)
# runConjunct(5, set_size = [4,12], method = 1, train = False)
# runMemSpan(5, target_size=[2,5], method = 1, train = True)




hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

print(hz)
core.quit()

