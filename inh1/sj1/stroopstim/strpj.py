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
expName='strpj'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(6) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `background` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `difficulty` INT(2) UNSIGNED NOT NULL,"
    "  `forePeriod` INT(4) UNSIGNED NOT NULL,"
    "  `resp` int(1) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"   
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `background`, `target`, `difficulty`, `forePeriod`, `resp`, `rt`)"
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
fpP=.35



######################
# Display Elements

def code(word,prop):
    return(word*4+prop*2)


def decode(cond):
    (word,temp) = divmod(cond,4)
    (x,prop) = divmod(temp,2)
    return(word,prop)

filename=[]



filename.append("SJ_RG_45.png")
filename.append("SJ_RG_52.png")
filename.append("SJ_RG_48.png")
filename.append("SJ_RG_55.png")
filename.append("SJ_GR_45.png")
filename.append("SJ_GR_55.png")
filename.append("SJ_GR_48.png")
filename.append("SJ_GR_52.png")
filename.append("SJ_BY_45.png")
filename.append("SJ_BY_52.png")
filename.append("SJ_BY_48.png")
filename.append("SJ_BY_55.png")
filename.append("SJ_YB_45.png")
filename.append("SJ_YB_52.png")
filename.append("SJ_YB_48.png")
filename.append("SJ_YB_55.png")

filedir='stroopstim/'

let=['f','j']
blank=visual.TextStim(window, text = "", pos = (0,0))

#####################

def doTrial(cond,fp):
        
    stim=visual.ImageStim(
        win=window,
        image=filedir+filename[cond])
    (word,prop) = decode(cond)
    respInt=-1
    duration=[1,fp,1]
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
    if (respInt== -1):
        wrongKeyText.draw()
        window.flip()
        wrongKey.play()
        event.waitKeys()
    elif (prop == 1 and ((word==0 and respInt==0) or (word==1 and respInt==1) or (word==2 and respInt==0) or (word==3 and respInt==1))):
        correct1.play()
        core.wait(0.1)
        correct2.play()
    else: 
        error.play()
        core.wait(0.8)
    
    return(respInt,rt)







############################################################
# Helper Text

breakTxt=visual.TextStim(window, text = "Take a Break\nPress any key to begin", pos = (0,0))
startTxt=visual.TextStim(window, text = "Welcome\nPosition your hands on the keys F (Red/Blue) and J (Green/Yellow) \nAny key to begin the PRACTICE ROUND", pos = (0,0))
warmUpDoneTxt=visual.TextStim(window, text = "That Was The Warm Up\n\nAny key to continue", pos = (0,0))
rgTxt=visual.TextStim(window, text = "Red (press f)      or       Green (press j)\n\nAny key to continue." , pos = (0,0))
modTxt=visual.TextStim(window, text = "Blue (press f)      or       Yellow (press j)\n\nAny key to continue." , pos = (0,0))

#########################
# Session Global Settings

N=16*2

cond=range(N)
for n in range(N):
    cond[n]=n%16
random.shuffle(cond)
fp = numpy.random.geometric(p=fpP, size=N)+30

pracN=1
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
    out=doTrial(pracCond[t],fpPrac[t])

warmUpDoneTxt.draw()
window.flip()
event.waitKeys()

for t in range(N):
    (blk,trl) = divmod(t,12)
    if trl==0 and blk>0:
        breakTxt.draw()
        window.flip()
        event.waitKeys()                 
    out=doTrial(cond[t],fp[t])
    rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
    (word,prop) = decode(cond[t])
    print (word,prop)
    addData = (sessionID, blk, t, word, prop, int(fp[t]), out[0], rt)
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
