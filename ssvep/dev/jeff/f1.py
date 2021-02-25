from psychopy import core, visual, sound, event
import os
import random
import sys
import decimal
import numpy as np
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *


#####################
# Experiment Settings
#####################


useDB=False
dbConf = beta
expName='flickflank1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `flankID` INT(2) UNSIGNED NOT NULL,"
    "  `targID` INT(2) UNSIGNED NOT NULL,"
    "  `resp` int(1) NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `flankID`, `targID`, `resp`, `rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s)")



############################################################


#####################
# Initialize 
if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1	

window=visual.Window(units= "pix", size =(640,320), rgb = "black", fullscr = False)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

#######################
# Trial Global Settings
numEvent=4
s0=visual.TextStim(window, text = "", pos = (0,0))
s1=visual.TextStim(window, text = "+", pos = (0,0))
s2=visual.TextStim(window, text = "", pos = (0,0))
duration=[1,60,30,30,1]
times=np.cumsum(duration)

#######################
# Feedback Global Settings
abortKey='9'
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.1)
error=sound.Sound(300,secs=.2)
wrongKey=sound.Sound(300,secs=1)
wrongKeyText=visual.TextStim(window, text = "Invalid Response\nRepostion Hands\nPress space to continue", pos = (0,0))
invalidResponse=2

#########################
# Session Global Settings

condStim=['AAA','HAH','AHA','HHH']
cond=np.repeat(range(4),3)
N=len(cond)
order=random.sample(range(N),N)

def decode(cond):
        (target,flanker) = divmod(cond,2)
        return(target,flanker)



def doTrial(cond):
    (target,flanker)=decode(cond)
    respInt=invalidResponse
    s3=visual.TextStim(window, text = condStim[cond], pos = (0,0))
    for frame in range(times[numEvent]):
        if (times[0]<=frame<times[1]): 
            s0.draw()
        if (times[1]<=frame<times[2]): 
            s1.draw()		
        if (times[2]<=frame<times[3]): 
            s2.draw()
        if (times[3]<=frame<times[4]): 
            s3.draw()
        window.flip()
    timer.reset()
    responseList = event.waitKeys()
    response = responseList[0][0]
    if (response==abortKey): exit()
    rt = timer.getTime()
    if (response=='a'): respInt=0
    if (response=='h'): respInt=1
    if (respInt== invalidResponse):
        wrongKeyText.draw()
        window.flip()
        wrongKey.play()
        event.waitKeys()
    elif (respInt==target):
        correct1.play()
        core.wait(0.1)
        correct2.play()
    else: 
        error.play()
    return(respInt,rt)


############################################################
# Start Experiment 

text=visual.TextStim(window, text = "Welcome\nf key for negative word\nj key for positive word\nany key to begin", pos = (0,0))
text.draw()
window.flip()
event.waitKeys()

for t in range(N):
	(target,flanker) =decode(cond[order[t]])
	out=doTrial(cond[order[t]])
	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, 1, t, cond[order[t]], target, flanker,out[0], rt)
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
