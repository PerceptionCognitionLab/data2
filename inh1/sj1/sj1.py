from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, sound, event
from PIL import Image
from psychopy.tools import imagetools
import mysql.connector
import os
import random
import sys
import datetime
import collections
import decimal
import time
import numpy
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

#####################
# Experiment Settings
#####################


useDB=False
dbConf = exp
expName='sj1'


createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `word` INT(2) UNSIGNED NOT NULL,"
    "  `col` INT(2) UNSIGNED NOT NULL,"
    "  `resp` int(1) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `word`, `col`, `resp`, `rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s)")

#####################
# Initialize 
if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1	

window=visual.Window(units= "pix", size =(1680, 1050), rgb = "grey", fullscr = False,)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)


#######################
# Feedback Global Settings
abortKey='9'
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.1)
error=sound.Sound(300,secs=.3)
wrongKey=sound.Sound(100,secs=1)
wrongKeyText=visual.TextStim(window, text = "Invalid Response\nRepostion Hands\nPress space to continue", pos = (0,0))
fpP=.35



######################
# Display Elements



def word():
	w = [1,2,3]
	w = numpy.random.choice(w)
    	return (w)

def stimulus(w):
    	if (w == 1):
        	im = Image.open('red.png')
    	elif (w == 2):
        	im = Image.open('green.png')
    	else : 
        	im = Image.open('blue.png')
    	im = im.convert('RGBA')
    	data = numpy.array(im)
    	length = len(data[numpy.where(data>0)])
    	K = int(.35*length)
    	L = int(.33*length)
    	arr = numpy.array([1] * K + [2]*L + [3]*(length - K - L))+250
    	numpy.random.shuffle(arr)
    	data[data>0]=arr
    	y = [1,2,3]
    	x = numpy.random.choice(y, 3, replace=False)+250
    	if (x[0] == 251):
       		col = 'red'
    	elif (x[1] == 251):
        	col = 'green'
    	else: 
       		col = 'blue'
    	red, green, blue, alpha = data.T
    	black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == x[0])
    	data[..., :-1][black_areas.T] = (255, 0, 0)
    	black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == x[1])
    	data[..., :-1][black_areas.T] = (0, 255, 0)
    	black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == x[2])
    	data[..., :-1][black_areas.T] = (0, 0, 255)
    	return(data,col)
	

let=['r','g','b']

#####################
blank=visual.TextStim(window, text = "+++", pos = (0,0))


def doTrial(cond):
	duration=[1,30,1]	
	z = word()
	j = stimulus(z)
	col = j[1]
	image = j[0]

	stim=visual.ImageStim(win=window, image=Image.fromarray(image), pos = (0,0))
	respInt=-1

	times=numpy.cumsum(duration)
	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			blank.draw()		
		if (times[1]<=frame<times[2]): 
			stim.draw()		
		window.flip()	
	timer.reset()
	responseList = event.waitKeys()
	response = responseList[0][0]
	if (response==abortKey): 
		exit()
	rt = timer.getTime()
	if (response==let[0]):
		respInt=0
	if (response==let[1]):
		respInt=1
	if (response==let[2]):
		respInt=2
	if (respInt== -1):
		wrongKeyText.draw()
		window.flip()
		wrongKey.play()
		event.waitKeys()
	elif ((col=='red' and respInt==0) or (col=='green' and respInt==1) or (col=='blue' and respInt==2)):
		correct1.play()
		core.wait(0.1)
		correct2.play()
	else: 
		error.play()
		core.wait(2)
	
	return(respInt,rt,z,col)







############################################################
# Helper Text

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome\nPosition your hands on the keys R G B \nAny key to begin the PRACTICE ROUND", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\nAny key to continue", pos = (0,0))
rgTxt=visual.TextStim(window, text = "Red (press R),  Blue (press B)    or  Green (press j)\n\nAny key to continue." , pos = (0,0))


#########################
# Session Global Settings

N=80*4

cond=range(N)
for n in range(N):
	cond[n]=n%16
random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30

pracN=8
pracCond=range(pracN)
for n in range(pracN):
	pracCond[n]=n%4
random.shuffle(pracCond)
fpPrac = numpy.random.geometric(p=fpP, size=pracN)+30

############################################################
# Start Experiment 

startTxt.draw()
window.flip()
event.waitKeys()

for t in range(pracN):				 
	out=doTrial(pracCond[t])

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()

for t in range(N):
	(blk,trl) = divmod(t,40)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()				 
	out=doTrial(cond[t])
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk, t, out[2], out[3], out[0], rt)
	if useDB:
		insertDatTable(insertTableStatement,addData,dbConf)
	else:
		print(addData)	



endText=visual.TextStim(window, text = "Thank You\nPlease See Experimenter", pos = (0,0))
endText.draw()
window.flip()
event.waitKeys(keyList=(abortKey))


##########################################################
# End Experiment


hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

core.quit()

