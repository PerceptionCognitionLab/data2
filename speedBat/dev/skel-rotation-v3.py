from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os
import copy as cp


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



def targetLetters(size):
	letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	x = random.choices(letters, k = size)
	for i in range(size):
		if x[i] in letters:
			letters.remove(x[i])
	if random.choice([0,1])==True:
		y = random.choice(x)
		z = True
	else:
		y = random.choice(letters)
		z = False
	x = "".join(x)
	return(x, y, z)
	


def runFrames(frame,frameTimes,timerStart=2):
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


def welcome():
	frameTime = [1, 1, 1]
	frame = []
	frame.append(visual.TextStim(win, "Welcome to the memory span experiment"))
	frame.append(visual.TextStim(win, "First you will a list of letters and followed by a single letter. \n If the letter was presented int eh list press m, otherwise enter x"))
	frame.append(visual.TextStim(win, "Press x or m to continue..."))
	runFrames(frame, frameTime, timerStart=2)	
	[resp,rt]=getResp(in_the_set = True)


rect = visual.Rect(
	win = win, 
	units = "pix",
	width = 40,
	height = 40, 
	lineColor = [0, 0, 0]
)


def curveLine(ang):
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
        text = f'Rotate {ang}\u00B0',
        pos = (0,250),
        color = 'white'
    )
    return(wedge,line1,line2,text_stim)



def rotMat(orig_mat, rotation, flip = False):
    rot_mat = orig_mat
    for r in range(rotation):
        rot_mat = np.rot90(rot_mat)
    if flip == True:
        ax = random.choice([0,1])
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





def runTrial(n=15):
    mats = []
    mats.append(np.array([[0,0,0],[1,1,0],[1,0,1]]))
    mats.append(np.array([[0,0,1],[1,0,0],[1,0,1]]))
    mats.append(np.array([[0,1,0],[1,0,1],[1,0,0]]))
    mats.append(np.array([[0,1,0],[1,0,0],[1,0,1]]))
    rots = []
    order = []
    for i in range(n):
        order.append(i%2)
        rots.append(i%2+1)
    random.shuffle(order)
    random.shuffle(rots)
    for t in range(15):
        if rots[t] == 1:
            [wedge90,line1,line2,txt] = curveLine(90)
        else:
            [wedge90,line1,line2,txt] = curveLine(180)
        if order[t] == 1:
            tmat = random.sample(mats,k=1)
            tmats = [tmat[0],rotMat(tmat[0],rots[t])]
        else:
            # tmat = random.sample(mats,k=2)
            # tmats = [tmat[0],rotMat(tmat[1],rots[t])]
            tmat = random.sample(mats,k=1)
            tmats = [tmat[0],rotMat(tmat[0],rots[t],flip=True)]
        stim = presMat(tmats[0], tmats[1])        
        stim.append(wedge90)
        stim.append(line1)
        stim.append(line2)
        stim.append(txt)
        trial(stim, order[t])





def trial(stims, truth):
    frameTimes=[30,30,1]  #at 60hz
    frame=[]
    #frame.append(visual.BufferImageStim(win, stim = stims))
    frame.append(visual.TextStim(win,"+"))
    frame.append(visual.TextStim(win,""))
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes)
    [resp,rt]=getResp(in_the_set = truth)
    acc=feedback(resp,1)
    print(truth,resp)


runTrial(n=15)




hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)


core.quit()
