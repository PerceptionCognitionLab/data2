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
expName='brightness1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `background` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `forePeriod` INT(4) UNSIGNED NOT NULL,"
    "  `resp` int(1) UNSIGNED NOT NULL,"
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

window=visual.Window(units= "pix", size =(1024,768), rgb = "grey", fullscr = False,)
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
def getFeedbackText(correct, score, nTrials):
	if (correct==True): 
		string=visual.TextStim(window, text = "Correct!\n\nScore: " + str(score) + "/" + str(nTrials), pos = (0,0))
	if (correct==False): 
		string=visual.TextStim(window, text = "Incorrect!\n\nScore: " + str(score) + "/" + str(nTrials), pos = (0,0))
	return(string)
	

	

########################
# Other Globals
fpP=.35
numTarg=8 
numBack=2  
numBackWarmUpBlanks=1 
targC=4
# present only difficult targets: 8 in total
usedTarg = range(2, 9) 


# only load in relevant stimuli for experiment
filename=[]
for n in usedTarg:
  filename.append("H_%02d.jpeg"%n)
for n in usedTarg:
  filename.append("A_%02d.jpeg"%n)

# load in relevant stimuli for warm up
filenameBlanks=[]
for n in usedTarg:
  filenameBlanks.append("blank_%02d.jpeg"%n)

filedir='../ahMorphStim/'

blank=visual.TextStim(window, text = "", pos = (0,0))
fix=visual.TextStim(window, text = "+", pos = (0,0))

#########################
# Condition Structure
def decode(cond):
	(back,targ) = divmod(cond,numTarg)
	return(back,targ)



#######################
# Trial Function
def doTrial(cond,fp,filename,feedback):
	(back,targ)=decode(cond)
	ans=1
	if (targ<targC): ans=0
	stim=visual.ImageStim(
		win=window,
		image=filedir+filename[cond])
	respInt=-1
	duration=[1,fp,10,1]
	times=numpy.cumsum(duration)
	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			fix.draw()		
		if (times[1]<=frame<times[2]): 
			stim.draw()
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
	if (respInt== -1):
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
		scoreText=getFeedbackText(True, score, feedback[1])
		scoreText.draw()
		window.flip()
	else: 
		error.play()
		# print score
		score=feedback[0]
		scoreText=getFeedbackText(False, score, feedback[1])
		scoreText.draw()
		window.flip()
                # time after error tone
		# core.wait(0.1)
        core.wait(0.5)
	return(respInt,rt,score)



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
lenWarmUp=16
rlWarmUp=[2,2,2,2,2,2,2,2]
condWarmUpAll=rld(rlWarmUp, numBack)
condWarmUpBlanks=rld(rlWarmUp, numBackWarmUpBlanks)
random.shuffle(condWarmUpAll)
random.shuffle(condWarmUpBlanks)

#########################
# Session Global Settings
lenBlock=10
nBlocks=8
N=nBlocks*lenBlock
fp=numpy.random.geometric(p=fpP, size=N)+30

# cond=range(N)
# for n in range(N):
# 	cond[n]=n%(numBack*numTarg)
# random.shuffle(cond)



############################################################
# Helper Text
breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome to our experiment!\n\nYour task is to identify as fast as possible the center letter as an A or an H by pressing the corresponding keys on the keyboard. You will receive auditory feedback on your responses.\n\nTo begin, place your fingers on the A and H letter of the keyboard, then press any key to begin the first warm up block.", pos = (0,0))
warmUpBlanksDoneTxt=visual.TextStim(window, text = "This was the first warm up block. In the next warm up bock you will see a 3 x 3 letter grid. Now, your task is to identify the center letter as fast as possible as an A or an H by pressing the corresponding keys on the keyboard. Base your response on the center letter alone and ignore the background context. You will receive auditory feedback on your responses. \n\nPress any key to begin the second warm up.", pos = (0,0))
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
	out=doTrial(condWarmUpBlanks[t],fp[t],filenameBlanks,feedback)
	feedback=[out[2],t+2]
	(back,targ)=decode(condWarmUpBlanks[t])
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
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
	out=doTrial(condWarmUpAll[t],fp[t],filename,feedback)
	feedback=[out[2],t+2]
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
		feedback=[0,trl+1] # reset score after each block
		breakTxt.draw()
		window.flip()
		event.waitKeys()					 
	out=doTrial(cond[t],fp[t],filename,feedback)
	feedback=[out[2],trl+2]
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
