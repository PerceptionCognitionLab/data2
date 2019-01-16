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
dbConf = beta
expName='globloc1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `task` INT(2) UNSIGNED NOT NULL,"  
    "  `diff` INT(2) UNSIGNED NOT NULL,"  
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `bigL` INT(2) UNSIGNED NOT NULL,"
    "  `smallL` INT(2) UNSIGNED NOT NULL,"
    "  `resp` int(1) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `task`, `diff`, `block`, `trial`, `bigL`, `smallL`, `resp`, `rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

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

prac=[]
easy=[]
mod=[]
dif=[]

dif.append("arb/aab.png")
dif.append("arb/arb.png")
dif.append("arb/rab.png")
dif.append("arb/rrb.png")
prac.append("st/ss.png")
prac.append("st/st.png")
prac.append("st/ts.png")
prac.append("st/tt.png")
easy.append("hox/hhx.png")
easy.append("hox/hox.png")
easy.append("hox/ohx.png")
easy.append("hox/oox.png")
mod.append("szn/ssn.png")
mod.append("szn/szn.png")
mod.append("szn/zsn.png")
mod.append("szn/zzn.png")

let=['f','j']

gName=[easy,mod,dif]

filedir='stim/'

blank=visual.TextStim(window, text = "", pos = (0,0))

#####################

def code(task,big,small):
	return(task*4+big*2+small)

def decode(cond):
	(task,filen) = divmod(cond,4)
	(big,small) = divmod(filen,2)
        return(task,big,small,filen)

def doTrial(cond):
	duration = [1,30,1]
	(task,big,small,filen) = decode(cond)	
	stim=visual.ImageStim(
		win=window,
		image=filedir+filename[filen])
	respInt=-1
	times=numpy.cumsum(duration)
	respInt=-1
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
	if (respInt== -1):
		wrongKeyText.draw()
		window.flip()
		wrongKey.play()
		event.waitKeys()
	elif ((task==0 and respInt==big) or (task==1 and respInt==small)):
#	elif (respInt==big):
		correct1.play()
		core.wait(0.1)
		correct2.play()

	return(respInt,rt)






############################################################
# Helper Text

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome\nPosition your hands on the keys F and J\nAny key to begin the PRACTICE ROUND", pos = (0,0))
startLrg=visual.TextStim(window, text = "Identify the LARGE letter", pos = (0,0))
startSml=visual.TextStim(window, text = "Identify the SMALL letter", pos = (0,0))
introTxt=visual.TextStim(window, text = "S (press f)      or       T (press j)\nAny key to begin", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\nAny key to continue", pos = (0,0))
easyTxt=visual.TextStim(window, text = "H (press f)      or       O (press j)\n\nAny key to continue." , pos = (0,0))
modTxt=visual.TextStim(window, text = "S (press f)      or       Z (press j)\n\nAny key to continue." , pos = (0,0))
difTxt=visual.TextStim(window, text = "A (press f)      or       R (press j)\n\nAny key to continue." , pos = (0,0))

#########################
# Session Global Settings

L=2
R=3
N=20
cond=range(N)
for n in range(N):
	cond[n]=n%4
random.shuffle(cond)

pracN=4*3
pracCond=range(pracN)
for n in range(pracN):
	pracCond[n]=n%4
random.shuffle(pracCond)

############################################################
# Start Experiment 


for l in range(L):
	startTxt.draw()
	window.flip()	
	event.waitKeys()
	if (l==0):
		startLrg.draw()
	if (l==1):
		startSml.draw()
		for n in range(N):
			cond[n]=n%4+4
		for n in range(pracN):
			pracCond[n]=n%4+4
	window.flip()	
	event.waitKeys()
	introTxt.draw()
	window.flip()
	event.waitKeys()

	filename=prac

	for t in range(pracN):
		out=doTrial(pracCond[t])

	warmUpDoneTxt.draw()
	window.flip()
	event.waitKeys()				 

	for r in range(R):
		filename=gName[r]
		random.shuffle(cond)
		if (l==0):
			startLrg.draw()
		if (l==1):
			startSml.draw()
		window.flip()
		event.waitKeys()				 	
		if (r==0):
			easyTxt.draw()
		elif (r==1):
			modTxt.draw()
		elif (r==2):
			difTxt.draw()
		window.flip()
		event.waitKeys()				 	
		for t in range(N):
			(blk,trl) = divmod(t,20)
			if trl==0 and blk>0:
				breakTxt.draw()
				window.flip()
				event.waitKeys()
			out=doTrial(cond[t])
    			rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
			(task,big,small,filen)=decode(cond[t])
			addData = (sessionID, l, r, blk, t, big, small, out[0], rt)
			if useDB:
				insertDatTable(insertTableStatement,addData,dbConf)
			else:
				print(addData)

	window.flip()				 
		

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
