from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np
from PIL import Image   
import os


numTarg = 6
numFlank = 2
flankVal=[0,1]
targVal=[0,.2,.4,.6,.8,1]


def decode(cond):
    return(divmod(cond,numFlank))

def code(targ,flank):
    return(targ*numFlank+flank)

condVals=np.array(range(numTarg*numFlank),dtype=int)
condRep=np.array([20,20,10,10,10,10,10,10,10,10,20,20],dtype=int)
condRep=np.array([1,1,1,1,1,1,1,1,1,1,1,1],dtype=int)
cond=np.repeat(condVals,condRep)
#np.random.shuffle(cond)
numTrialsPerBlock = 40


resX=100
resY=110

sepX=resX+10
sepY=resY+10
posX=sepX*np.array((-1,0,1))
posY=sepY*np.array((-1,0,1))

##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = exp
expName='brightFlank1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `flanker` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `resp` INT(1) NOT NULL,"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `flanker`, `target`, `resp`,`rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s)")

if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
########################################
# GLOBAL SETTINGS  #####################
########################################
window=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(400,400),
                     color=[0,0,0],
                     fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.1)
error=sound.Sound(300,secs=.2)
####################################
##  TRIAL SET UP   #################
####################################

    


def makeArray(p,mx,my):
    n=mx*my
    x=int((1-p)*n+.5)
    a0=np.zeros(x,dtype=np.uint8)
    a1=np.ones(n-x,dtype=np.uint8)
    a2=np.concatenate((a0,255*a1))
    np.random.shuffle(a2)
    a3=np.reshape(a2,(my,mx))
    return(Image.fromarray(a3))


def doTrial(cond):
    blank=visual.TextStim(win=window,text="")
    
    [targ,flank]=decode(cond)
    im=[]
    for x in range(3):
        for y in range(3):
            t=makeArray(flankVal[flank],resX,resY)
            im.append(visual.ImageStim(win=window,
                               pos=(posX[x],posY[y]),
                               image=t))
    im[4].image=makeArray(targVal[targ],resX,resY)        
    full=visual.BufferImageStim(win=window,stim=im)

    correct=int(targVal[targ]>.5)
    
    blank.draw()
    window.flip()
    core.wait(.5)        
    timer.reset()
    full.draw()
    window.flip()
    window.getMovieFrame(buffer='front')
    keys=event.waitKeys(keyList=['z','slash','9'],timeStamped=timer)
    blank.draw()
    window.flip()
    resp=keys[0][0]
    rt=keys[0][1]
    if resp=='9':
        window.close()
        core.quit()
        exit()
    if resp=='z':
        respInt=0
    else:
        respInt=1
    if respInt==correct:
        correct1.play()
        core.wait(0.1)
        correct2.play()
    else:
        error.play()
    core.wait(.5)
    return(respInt,rt)

#######################################
### START EXPERIMENT ##################
#######################################

numTrials=len(cond)

for n in range(numTrials):
    (blk,trl)=divmod(n,numTrialsPerBlock)
    if (trl==0):
        st0=visual.TextStim(window, text="z: more black dots",
                            color=(-1,-1,-1),
                            pos=(0,50))
        st1=visual.TextStim(window, text="/: more white dots",
                            color=(1,1,1),
                            pos=(0,-50))
        st0.draw()
        st1.draw()
        window.flip()
        event.waitKeys(keyList=['z','slash','9'])
    (respInt,RT)=doTrial(cond[n])
    rt = decimal.Decimal(RT).quantize(decimal.Decimal('1e-3'))
    (targ,flank)=decode(cond[n])
    addData = (sessionID,blk,trl,flank,targ,respInt,rt)
    if useDB:
        insertDatTable(insertTableStatement,addData,dbConf)
    else:
        print(addData)	

window.saveMovieFrames("display.png")
hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)
core.quit()


