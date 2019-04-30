from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, sound, event
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


useDB=True
dbConf = exp
expName='as4'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `cue` INT(2) UNSIGNED NOT NULL,"
    "  `location` INT(2) UNSIGNED NOT NULL,"
    "  `forePeriod` INT(4) UNSIGNED NOT NULL,"
    "  `targetTime` INT(4) UNSIGNED NOT NULL,"
    "  `resp` int(1) NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `target`, `cue`, `location`, `forePeriod`, `targetTime`, `resp`, `rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


############################################################


#####################
# Initialize 
if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1	

window=visual.Window(units= "pix", size =(1024,768), rgb = "black", fullscr = True,)
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




#########################
# Trial Functions & Globals



pos = ((-200,-100),(-200,100),(200,100),(200,-100))
arrowVert = [(-30,7),(-30,-7),(-0,-7),(-0,-15),(30,0),(0,15),(0,7)]
targets=["1","2","3","4"]
duration = [1,30,-1,6,-1,-1,1,1]
fpEvent = 2
targEvent =5
targTime=8
targCue = 4
targCueI = 15
targCueC = 7
fpP=.35

blank=visual.TextStim(window, text = "", pos = (0,0))
fix=visual.TextStim(window, text = "+", pos = (0,0))
cueCirc=visual.Circle(window,fillColor="Red",pos=(0,0),radius=30)
circ=visual.Circle(window,pos=(0,0),radius=30,lineColor='white')
mask1=visual.TextStim(window,text="@",pos = (0,0))
mask2=visual.TextStim(window,text="#",pos = (0,0))



def decode(cond):
	(targ,temp) = divmod(cond,8)
	(loc,cue) = divmod(temp,2)
	#cue=numpy.random.rand()<.6
	return(targ,cue,loc)

def doTrial(cond,fpTime,targCueI,targCueC,targTime):
	(targ,cue,loc) = decode(cond)
	cueCirc.pos=pos[(loc+2)%4]
	duration[fpEvent] = fpTime
	duration[targEvent] = targTime
	if cue: 
		duration[targCue] = targCueI
	else:
		duration[targCue] = targCueC
	times=numpy.cumsum(duration)
	target=visual.TextStim(window, text = targets[targ],pos=pos[loc])
	mask1.pos=pos[loc]
	mask2.pos=pos[loc]
	circ.pos=pos[loc]
	respInt=-1
	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			blank.draw()		
		if (times[1]<=frame<times[2]): 
			fix.draw()
		if (times[2]<=frame<times[3]): 
			blank.draw()	
		if (times[3]<=frame<times[4]):
 
			if cue: 
				cueCirc.draw()

			else:
				circ.draw()

						
		if (times[4]<=frame<times[5]): 
			target.draw()

		if (times[5]<=frame<times[6]): 
			mask1.draw()
		if (times[6]<=frame<times[7]): 
			mask2.draw()
		window.flip()
	timer.reset()
	responseList = event.waitKeys()
	response = responseList[0][0]
	if (response==abortKey): 
		exit()
	rt = timer.getTime()
	if (response=='1'): 
		respInt=0
	if (response=='2'):
		respInt=1
	if (response=='3'):
		respInt=2
	if (response=='4'):
		respInt=3
	if (respInt== -1):
		wrongKeyText.draw()
		window.flip()
		wrongKey.play()
		event.waitKeys()
	elif (respInt==targ):
		correct1.play()
		core.wait(0.1)
		correct2.play()
	else: 
		error.play()
	return(respInt,rt)





#########################
# Session Global Settings

N=320
cond=range(N)
for n in range(N):
	cond[n]=n%32
random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30
pracN=16
pracCond=range(16)
random.shuffle(pracCond)




############################################################
# Helper Text

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome\nIdentify the Number (1 through 4)\nAny key to begin", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\n Identify the Number (1 through 4)\nAny key to begin", pos = (0,0))


############################################################
# Start Experiment 


startTxt.draw()
window.flip()
event.waitKeys()

for t in range(pracN):				 
	out=doTrial(pracCond[t],35,20,20,20)

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()				 



for t in range(N):
	(blk,trl) = divmod(t,64)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()				 
	out=doTrial(cond[t],fp[n],targCueI, targCueC, targTime)
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	(targ,cue,loc) = decode(cond[t])
	#print (targ,cue,loc)
	addData = (sessionID, blk, t, targ, cue, loc, int(fp[t]), targTime, out[0], rt)
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
