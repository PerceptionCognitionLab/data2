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
LeftLet = ['H', 'S', 'A','S']
RightLet = ['O', 'Z' , 'R','T']

def leftL(Letters):
	left=visual.TextStim(window, text = Letters, pos = (-400,0), height = 50)
	return(left)

def rightL(Letters):
	right=visual.TextStim(window, text = Letters, pos = (400,0),height = 50)
	return(right)
#####################

def code(big,small):
	return(big*2+small)

def decode(cond):
	(big,small) = divmod(cond,2)
        return(big,small)

def codeT(task,diff):
	return(task*3+diff)

def decodeT(condT):
	(task,diff) = divmod(condT,3)
	return(task,diff)

def doTrial(cond):
	duration = [1,30,1]
	(big,small) = decode(cond)	
	stim=visual.ImageStim(
		win=window,
		image=filedir+filename[cond])
	respInt=-1
	times=numpy.cumsum(duration)
	for frame in range(max(times)):
		if (times[0]<=frame<times[1]):
			blank.draw()		
		if (times[1]<=frame<times[2]):
			left = leftL(LeftLet[diff])
			right = rightL(RightLet[diff])
			left.draw()
			right.draw() 
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
	else: 
		error.play()
		core.wait(1)

	return(respInt,rt)






############################################################
# Helper Text
startTxt=visual.TextStim(window, text = "Welcome\nPosition your hands on the keys F and J\nYou will see a LARGE letter made of SMALL letters \n Your task is to identify the LARGE or the SMALL letter\nThe letters are displayed on the screen\n LEFT letter = press F       RIGHT letter = press J\nPress any key to begin the practice round", pos = (0,0))

startLrg=visual.TextStim(window, text = "Identify the LARGE letter\n\nPress any key to start", pos = (0,0))
startSml=visual.TextStim(window, text = "Identify the SMALL letter\n\nPress any key to start", pos = (0,0))

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
largeBreak=visual.TextStim(window, text = "Take a long Break\nWait for the next task", pos = (0,0))

warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\nIn the remaining trials there will also be background noise\n Identify the LARGE letter, or the SMALL letters that make the large letter.\n\nAny key to continue", pos = (0,0))


#########################
# Session Global Settings

L=2
R=3
N=20
condT=range(L*R)
random.shuffle(condT)

cond=range(N)
for n in range(N):
	cond[n]=n%4
random.shuffle(cond)

pracCondT=2
pracN=4*3
pracCond=range(pracN)
for n in range(pracN):
	pracCond[n]=n%4
random.shuffle(pracCond)

############################################################
# Start Experiment 

startTxt.draw()
window.flip()	
event.waitKeys()
filename=prac
for b in range(pracCondT):
	task=b
	diff=3
	left = leftL(LeftLet[diff])
	right = rightL(RightLet[diff])
	if (task==0):	
		startLrg.draw()			
		left.draw()
		right.draw() 
	if (task==1):
		startSml.draw()
		left.draw()
		right.draw() 
	window.flip()	
	event.waitKeys()
	for t in range(pracN):
		out=doTrial(pracCond[t])

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()

for b in range(L*R):
	(task,diff)=decodeT(condT[b])
	left = leftL(LeftLet[diff])
	right = rightL(RightLet[diff])
	if (task==0):	
		startLrg.draw()
		left.draw()
		right.draw()
	if (task==1):
		startSml.draw()
		left.draw()
		right.draw() 
	window.flip()	
	event.waitKeys()				 
	filename=gName[diff]
	random.shuffle(cond)				 	
	for t in range(N):
		(blk,trl) = divmod(t,40)
		if trl==0 and blk>0:
			breakTxt.draw()
			window.flip()
			event.waitKeys()
		out=doTrial(cond[t])
    		rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
		(big,small)=decode(cond[t])
		addData = (sessionID, task, diff, blk, t, big, small, out[0], rt)
		if useDB:
			insertDatTable(insertTableStatement,addData,dbConf)
		else:
			print(addData)
	largeBreak.draw()
	window.flip()			 
	core.wait(10)

		

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
