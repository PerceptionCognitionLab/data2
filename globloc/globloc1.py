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
dbConf = beta
expName='idgb1'

#####################
# Initialize 
if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1	

window=visual.Window(units= "pix", size =(1024,768), rgb = "black", fullscr = False,)
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



######################
# Display Elements
targPng=#png images + extra condition for trial
targLet=["s","t","x"]
masks=#png masks
duration = [1,30,-1,-1,1]
fpEvent = 2
targEvent =3
targTime=7
fpP=.35

blank=visual.TextStim(window, text = "", pos = (0,0))
fix=visual.TextStim(window, text = "+", pos = (0,0))

#####################
#
#decode depends on conditions included
# not necessary?? condition can be linked to file name
# for storing this can be nice
#def decode(cond):
#	(large,temp) = divmod(cond,4)
#	(small,ref) = divmod(temp,2)
#	return(large,small,ref)


def doTrial(cond,fpTime,targTime):
	duration[fpEvent] = fpTime
	duration[targEvent] = targTime
#maybe (large,small,ref)=decode(cond)
	times=numpy.cumsum(duration)
	respInt=-1
	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			blank.draw()		
		if (times[1]<=frame<times[2]): 
			fix.draw()	
		if (times[2]<=frame<times[3]): 
			#png targPng[cond]
		if (times[3]<=frame<times[4]): 
			#png mask
		window.flip()
	timer.reset()
	responseList = event.waitKeys()
	response = responseList[0][0]
	if (response==abortKey): 
		exit()
	rt = timer.getTime()
	if (response==targLet[0]): 
		respInt=0
	if (response==targLet[1]):
		respInt=1
	if (response==targLet[2]):
		respInt=2
	if (respInt== -1):
		wrongKeyText.draw()
		window.flip()
		wrongKey.play()
		event.waitKeys()
	return(respInt,rt)

#########################
# Session Global Settings

N=160
cond=range(N)
for n in range(N):
	cond[n]=n%8
random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30
pracN=16
pracCond=range(pracN)
for n in range(pracN):
	pracCond[n]=n%8
random.shuffle(pracCond)




############################################################
# Helper Text

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome\nIdentify the Large Letter (s, t, x)\nAny key to begin", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\n Identify the Large Letter (s, t, x)\nAny key to begin", pos = (0,0))


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
	(blk,trl) = divmod(t,40)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()				 
	out=doTrial(cond[t],fp[n],targTime)
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk, t, large, small, ref, int(fp[t]), int(targTime), out[0], rt)
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
