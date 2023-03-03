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
	width = 20,
	height = 20, 
	lineColor = [0, 0, 0]
)

mat = np.array([[1,0,0],[0,0,1],[0,0,0]])

def rotation(orig_mat, rotation):
	stims = []
	rot_mat = orig_mat
	for r in range(rotation):
		rot_mat = np.rot90(rot_mat)
	y = 100 		
	for r in range(3):
		x1 = -200
		x2 = 200
		for c in range(3):
			trect = cp.copy(rect)
			if orig_mat[r,c] == 1:
				trect.fillColor = [1,-1,-1]
			else:
				trect.fillColor = [-1,-1,1]
			trect.pos = [x1,y]
			stims.append(trect)
			trect2 = cp.copy(rect)
			x1+=20
			if rot_mat[r,c] == 1:
				trect2.fillColor = [1,-1,-1]
			else:
				trect2.fillColor = [-1,-1,1]
			trect2.pos = [x2,y]
			stims.append(trect2)
			x2+=20
		y+=20
	return(stims)
	

stims = rotation(mat, 1)
#print(stims)




def trial(set_size):
	frameTimes=[60,30,60,1]  #at 60hz
	[target, q, in_the_set] = targetLetters(set_size)
	frame=[]
	#frame.append(visual.BufferImageStim(win, stim = stims))
	frame.append(rect)	
	frame.append(visual.TextStim(win,target))
	frame.append(visual.TextStim(win,""))
	frame.append(visual.TextStim(win,q))
	runFrames(frame,frameTimes)
	[resp,rt]=getResp(in_the_set = in_the_set)
	acc=feedback(resp,1)
	print(rt, resp)


a=visual.TextStim(win,"Here")
b=visual.TextStim(win,"There",pos=[40,50])

a = cp.copy(rect)
a.pos = [100,-100]
a.fillColor = [-1,-1,1]
b = cp.copy(rect)
b.pos = [100,100]
b.fillColor = [1,-1,-1]
c=visual.BufferImageStim(win,stim=stims)
c.draw()

win.flip()
event.waitKeys()

welcome()
for i in range(3,10):
	trial(i)

hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)


core.quit()
