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


useDB=False
dbConf = exp
expName='acstr'

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
poslist=[(-400,300), (400,300), (-400, -300), (400,-300)]
arrowOrient=[180-31.7,180+31.7,-31.7,31.7]
arrowVert = [(-30,7),(-30,-7),(-0,-7),(-0,-15),(30,0),(0,15),(0,7)]
targets=["1","2","3","4"]
duration = [1,60,-1,40,30,0,1,1]
fpEvent = 2
targEvent =5
targTime=7
fpP=.35

blank=visual.TextStim(window, text = "", pos = (0,0))
fix=visual.TextStim(window, text = "+", pos = (0,0))


cornsize=75
midsize=75
numsize=40


mask1=visual.TextStim(window,text="#",pos = poslist[0], height=numsize)
mask2=visual.TextStim(window,text="#",pos = poslist[1], height=numsize)
mask3=visual.TextStim(window,text="#",pos = poslist[2], height=numsize)
mask4=visual.TextStim(window,text="#",pos = poslist[3], height=numsize)



arrow = visual.ShapeStim(window, vertices=arrowVert, size=1, lineColor='red')





c1=visual.TextStim(window, text="RED", pos=poslist[0], height=cornsize)
c2=visual.TextStim(window, text="GREEN", pos=poslist[1], height=cornsize)
c3=visual.TextStim(window, text="BLUE", pos=poslist[2], height=cornsize)
c4=visual.TextStim(window, text="YELLOW", pos=poslist[3], height=cornsize)

c1.size=.5

cstrings=["RED", "GREEN", "BLUE", "YELLOW"]
ccols=[(1,0,0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]



def colword(wd, col):
	return(visual.TextStim(window, text=cstrings[wd], pos=(0,0), color=ccols[col], colorSpace='rgb', height=midsize) )

def decode(cond):
	(targ,temp) = divmod(cond,8)
	(loc,cue) = divmod(temp,2)
	return(targ,cue,loc)

def doTrial(cond,fpTime,targTime):
	duration[fpEvent] = fpTime
	duration[targEvent] = targTime
	times=numpy.cumsum(duration)
	(targ,cue,loc) = decode(cond)
	target=visual.TextStim(window, text = targets[targ],pos=pos[loc])
	respInt=-1

	w=numpy.random.randint(4)
	c=numpy.random.randint(4)
	cw=colword(w,c)

	leperm=numpy.random.permutation(4)
	
	n1=visual.TextStim(window, text=targets[leperm[0]], pos=poslist[0], height=numsize)
	n2=visual.TextStim(window, text=targets[leperm[1]], pos=poslist[1], height=numsize)
	n3=visual.TextStim(window, text=targets[leperm[2]], pos=poslist[2], height=numsize)
	n4=visual.TextStim(window, text=targets[leperm[3]], pos=poslist[3], height=numsize)

	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()		
		if (times[1]<=frame<times[2]):
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()



			cw.draw()
		if (times[2]<=frame<times[3]): 
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()	
		if (times[3]<=frame<times[4]):
 			n1.draw()
 			n2.draw()
 			n3.draw()
 			n4.draw()
						
		if (times[4]<=frame<times[7]): 
			mask1.draw()
			mask2.draw()
			mask3.draw()
			mask4.draw()
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
	elif (respInt==leperm[c]):
		correct1.play()
		core.wait(0.1)
		correct2.play()
	else: 
		error.play()
	return(respInt,rt, w, c, leperm)





#########################
# Session Global Settings

N=40
cond=range(N)
for n in range(N):
	cond[n]=n%32
random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30
pracN=4
pracCond=range(32)
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
	out=doTrial(pracCond[t],35,20)

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()				 



for t in range(N):
	(blk,trl) = divmod(t,64)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()				 
	out=doTrial(cond[t],fp[n],targTime)
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
#	(targ,cue,loc) = decode(cond[t])
	#print (targ,cue,loc)
	addData = (sessionID, blk, t, out[2], out[3], out[4][0], out[4][1], out[4][2], out[4][3], out[0], rt)
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
