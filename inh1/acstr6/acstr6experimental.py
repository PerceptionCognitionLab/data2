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
expName='acstr6'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `WordInt` INT(1) UNSIGNED NOT NULL,"
    "  `ColorInt` INT(1) UNSIGNED NOT NULL,"
    "  `TrueInt` INT(1) UNSIGNED NOT NULL,"
    "  `Cong` INT(1) UNSIGNED NOT NULL,"
    "  `Correct` INT(1) UNSIGNED NOT NULL,"
    "  `Response` INT(1) NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `WordInt`, `ColorInt`, `TrueInt`, `Cong`, `Correct`,  `Response`, `rt`)"
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
poslistcorners=[(-500,400), (500,400), (-500, -400), (500,-400)]
arrowOrient=[180-31.7,180+31.7,-31.7,31.7]
arrowVert = [(-30,7),(-30,-7),(-0,-7),(-0,-15),(30,0),(0,15),(0,7)]
targets=["1","2","3","4"]
duration = [1,40,-1,9,-1,-1,1,1]
fpEvent = 2
targEvent =5
targTime=7
wordEvent=4
wordTime=27
wordTimeRed=17
#17
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


box1=visual.TextStim(window,text="[  ]",pos = poslist[0], height=numsize)
box2=visual.TextStim(window,text="[  ]",pos = poslist[1], height=numsize)
box3=visual.TextStim(window,text="[  ]",pos = poslist[2], height=numsize)
box4=visual.TextStim(window,text="[  ]",pos = poslist[3], height=numsize)

arrow = visual.ShapeStim(window, vertices=arrowVert, size=1, lineColor='red')





c1=visual.TextStim(window, text="RED", pos=poslistcorners[0], height=cornsize)
c2=visual.TextStim(window, text="GREEN", pos=poslistcorners[1], height=cornsize)
c3=visual.TextStim(window, text="BLUE", pos=poslistcorners[2], height=cornsize)
c4=visual.TextStim(window, text="YELLOW", pos=poslistcorners[3], height=cornsize)

c1.size=.5

cstrings=["RED", "GREEN", "BLUE", "YELLOW"]
ccols=[(1,0,.2), (0, 1, 0), (0, .3, 1), (1, 1, 0)]



def colword(wd, col):
	return(visual.TextStim(window, text=cstrings[wd], pos=(0,0), color=ccols[col], colorSpace='rgb', height=midsize) )

def decode(cond):
	(targ,temp) = divmod(cond,8)
	(loc,cue) = divmod(temp,2)
	return(targ,cue,loc)

def doTrial(cond,fpTime,targTime, wordTime):
	duration[fpEvent] = fpTime
	duration[targEvent] = targTime

	(targ,cue,loc) = decode(cond)
	target=visual.TextStim(window, text = targets[targ],pos=pos[loc])
	respInt=-1
	
	if (cond==1):
		w=numpy.random.randint(4)
		c=w
		duration[wordEvent] = wordTime
	elif (cond==2):
		w=numpy.random.randint(4)
		c=w
		duration[wordEvent] = wordTimeRed
	else:
		w=numpy.random.randint(4)
		c=numpy.random.randint(3)
		duration[wordEvent] = wordTime
		if (c==w):
			c+=1
	times=numpy.cumsum(duration)
	#w=numpy.random.randint(4)
	#c=numpy.random.randint(4)
	cw=colword(w,c)

	leint=numpy.random.randint(4)
	leperm=['X', 'X', 'X', 'X']
	leperm[c]=leint+1
#	leperm=numpy.random.permutation(4)
	
	n1=visual.TextStim(window, text=str(leperm[0]), pos=poslist[0], height=numsize)
	n2=visual.TextStim(window, text=str(leperm[1]), pos=poslist[1], height=numsize)
	n3=visual.TextStim(window, text=str(leperm[2]), pos=poslist[2], height=numsize)
	n4=visual.TextStim(window, text=str(leperm[3]), pos=poslist[3], height=numsize)

	for frame in range(max(times)):
		if (times[0]<=frame<times[2]):
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()
			box1.draw()
			box2.draw()
			box3.draw()
			box4.draw()		
		if (times[2]<=frame<times[3]):
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()
			box1.draw()
			box2.draw()
			box3.draw()
			box4.draw()


			cw.draw()
		if (times[3]<=frame<times[4]): 
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()
			box1.draw()
			box2.draw()
			box3.draw()
			box4.draw()	
		if (times[4]<=frame<times[5]):
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()
			box1.draw()
			box2.draw()
			box3.draw()
			box4.draw()
 			n1.draw()
 			n2.draw()
 			n3.draw()
 			n4.draw()
						
		if (times[5]<=frame<times[7]): 
			c1.draw()
			c2.draw()
			c3.draw()
			c4.draw()
			box1.draw()
			box2.draw()
			box3.draw()
			box4.draw()
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
		iscorrect=2
	elif (respInt==leint):
		correct1.play()
		core.wait(0.1)
		correct2.play()
		iscorrect=1
	else: 
		iscorrect=0
		error.play()
	return(respInt,rt, w, c, leint, cond, iscorrect)





#########################
# Session Global Settings

N=480
perccong=2/3

cond=range(N)
for n in range(N):
	if n<(round(perccong*.5*N)):
		cond[n]=1
	elif n<(round(perccong*N)):
		cond[n]=2
	else:
		cond[n]=0

random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30
pracN=4
pracCond=range(16)

for n in range(pracN):
	if n%2==0:
		pracCond[n]=0
	else:
		pracCond[n]=1


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
	out=doTrial(pracCond[t],35,40, 20)

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()				 



for t in range(N):
	(blk,trl) = divmod(t,80)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()				 
	out=doTrial(cond[t],fp[n],targTime, wordTime)
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
#	(targ,cue,loc) = decode(cond[t])
	#print (targ,cue,loc)
	addData = (sessionID, blk, t, out[2], out[3], out[4], out[5], out[6], out[0], rt)
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
