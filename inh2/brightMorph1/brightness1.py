from psychopy import prefs
prefs.general['audioLib'] = ['PTB']
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
expName='brightness1'
checkExp(expName,dbConf)

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `background` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `forePeriod` INT(4) UNSIGNED NOT NULL,"
    "  `resp` INT(1) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `background`, `target`, `forePeriod`, `resp`, `rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")


############################################################


#####################
# Initialize 
if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1	

# dim: 1680x1050
window=visual.Window(units= "pix", size =(1024,768), color = [-1,-1,-1], fullscr = False)
grating1 = visual.GratingStim(win=window, size=(2000,2000),sf=0.01,ori=45,contrast=.2,opacity=1)
grating2 = visual.GratingStim(win=window, size=(2000,2000),sf=0.01,ori=135,contrast=.2,opacity=.5)
noise1=visual.NoiseStim(win=window,units='pix',noiseType='white', size=(1650,1050),opacity=.3)
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
wrongKeyText=visual.TextStim(window, text = "Invalid Response\nRepostion Hands\nPress space to continue", pos = (0,0), color=[-1])

def getFeedbackText(correct, score, nTrials):
	if (correct==True): 
		string=visual.TextStim(window, text = "Correct!\n\nScore: " + str(score) + "/" + str(nTrials), pos = (0,0), color=[-1])
	if (correct==False): 
		string=visual.TextStim(window, text = "Incorrect!\n\nScore: " + str(score) + "/" + str(nTrials), pos = (0,0),color=[-1])
	return(string)
	

	

########################
# Other Globals
fpP=.35
numTarg=8 
numBack=2  
numBackWarmUpBlanks=1 
targC=4
# present only difficult targets: 8 in total
usedTarg = range(1, 9) 


# define relevant stimuli for the experiment
backColors=[-0.7, 0.7]
radius=[500,200]
targColors=[-0.36,-0.27,-0.18,-0.09,0.09,0.18,0.27,0.36]

blank=visual.TextStim(window, text = "", pos = (0,0))
fix=visual.TextStim(window, text = "+", pos = (0,0), color=[-1])

##########################
# Draw the circles

def drawCircle(window, color, radius):
	circleColor=numpy.repeat(color,3).tolist()
	circle=visual.Circle(
	    win=window,
	    units="pix",
	    radius=radius,
	    fillColor=circleColor,
	    lineColor=circleColor,
	    edges=180)
	return(circle)

#########################
# Condition Structure
def decode(cond):
	(back,targ) = divmod(cond,numTarg)
	return(back,targ)

#######################
# Trial Function
def doTrial(cond,fp,backColors,targColors,feedback):
	(back,targ)=decode(cond)
	ans=1
	if (targ<targC): ans=0
	targCircle=drawCircle(window, targColors[targ], radius=radius[1])
	respInt=-1
	duration=[1,fp,10,1]
	times=numpy.cumsum(duration)
	for frame in range(max(times)):
		grating1.draw()
		grating2.draw()
		noise1.draw()
		if (times[0]<=frame<times[1]): 
			fix.draw()		
		if (times[1]<=frame<times[2]):
			if(backColors is not None):
				backCircle=drawCircle(window, backColors[back], radius=radius[0])
				backCircle.draw()
			targCircle.draw()
		if (times[2]<=frame<times[3]): 
			blank.draw()
		window.flip()
	timer.reset()
	responseList = event.waitKeys()
	response = responseList[0][0]
	if (response==abortKey): 
		exit()
	rt = timer.getTime()
	if (response=='a'): 
		respInt=1
	if (response=='h'):
		respInt=0
	# Feedback text
	grating1.draw()
	grating2.draw()
	noise1.draw()
	if (respInt== -1):
		score=feedback[0]
		roundNr=feedback[1]
		wrongKeyText.draw()
		window.flip()
		wrongKey.play()
		event.waitKeys()
	elif (respInt==ans):
		#correct1.play()
                # adjust time between tones
		#core.wait(0.1)
		correct2.play()
		# print score
		score=feedback[0]+1
		roundNr=feedback[1]+1
		scoreText=getFeedbackText(True, score, feedback[1])
		scoreText.draw()
		window.flip()
	else: 
		error.play()
		# print score
		score=feedback[0]
		roundNr=feedback[1]+1
		scoreText=getFeedbackText(False, score, feedback[1])
		scoreText.draw()
		window.flip()
                # time after error tone
		# core.wait(0.1)
	core.wait(0.5)
	return(respInt,rt,score,roundNr)


#########################
# Run length decoding
def rld(rl, numBack):
	cond = range(len(rl)*numBack)
	rlAll=rl*numBack
	output = numpy.repeat(cond, rlAll, axis=0)
	return(output.tolist())

# experimental block: 480 trials
rl=[30,30,30,30,30,30,30,30]
cond=rld(rl, numBack)
random.shuffle(cond)

# warm up blocks: 10 trials each
lenWarmUp=2
rlWarmUp=[2,2,2,2,2,2,2,2]
condWarmUpAll=rld(rlWarmUp, numBack)
condWarmUpBlanks=rld(rlWarmUp, numBackWarmUpBlanks)
random.shuffle(condWarmUpAll)
random.shuffle(condWarmUpBlanks)

#########################
# Session Global Settings
lenBlock=60
nBlocks=8
N=nBlocks*lenBlock
fp=numpy.random.geometric(p=fpP, size=N)+30

############################################################
# Helper Text
breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome to our experiment!\n\nYour task is to identify as accurate and as fast as possible the circle as bright or dark by pressing either 'A' (if you think the circle is bright) or 'H' (if you think the circle is dark) on the keyboard. You will receive feedback on your responses.\n\nTo begin, place your fingers on the A and H letter of the keyboard, then press any key to begin the first warm up block.", pos = (0,0))
warmUpBlanksDoneTxt=visual.TextStim(window, text = "This was the first warm up block. In the next warm up bock you will see two circles. Now, your task is to identify the inner circle as accurate and as fast as possible as light or dark by pressing either 'A' (if you think the circle is bright) or 'H' (if you think the circle is dark) on the keyboard. Base your response on the inner circle alone and ignore the background context. You will receive feedback on your responses. \n\nPress any key to begin the second warm up.", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That was the warm up.\n\nPress any key to begin the real experiment.", pos = (0,0))
endText=visual.TextStim(window, text = "Thank You!\nThis is the end of the experiment.\nPlease See The Experimenter.", pos = (0,0))



############################################################
# Start Experiment
startTxt.draw()
window.flip()
event.waitKeys()

# Warm up trial 1: only show blanks
feedback=[0,1]	
for t in range(lenWarmUp):
	(blk,trl) = divmod(t,lenWarmUp)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()					 
	out=doTrial(condWarmUpBlanks[t],fp[t],None,targColors,feedback)
	feedback=[out[2],out[3]]
	(back,targ)=decode(condWarmUpBlanks[t])
	rt=decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk,trl,back,targ, int(fp[t]), out[0], rt)

warmUpBlanksDoneTxt.draw()
window.flip()
event.waitKeys()

# Warm up trial: present experimental stimuli
feedback=[0,1]	
for t in range(lenWarmUp):
	(blk,trl) = divmod(t,lenWarmUp)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()					 
	out=doTrial(condWarmUpAll[t],fp[t],backColors,targColors,feedback)
	feedback=[out[2],out[3]]
	(back,targ)=decode(condWarmUpAll[t])
	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk,trl,back,targ, int(fp[t]), out[0], rt)

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()				 

# experimental blocks
feedback=[0,1]	
for t in range(N):
	(blk,trl) = divmod(t,lenBlock)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()					 
	out=doTrial(cond[t],fp[t],backColors,targColors,feedback)
	feedback=[out[2],out[3]]
	(back,targ)=decode(cond[t])
	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk,trl,back,targ, int(fp[t]), out[0], rt)
	if useDB:
		insertDatTable(insertTableStatement,addData,dbConf)
	else:
		print(addData)	

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
