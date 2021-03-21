from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np
from PIL import Image   
import os



##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = exp
expName='brFlank-p1'

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
                     size=(600,600),
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

    
blank=visual.TextStim(win=window,text="")
grate= visual.GratingStim(win=window,sf=.05,size=256,mask="gauss",
                              ori=1,opacity=.3)
noise=visual.NoiseStim(win=window,size=(256,256),noiseType="uniform",
                           noiseElementSize=2,opacity=0)




def doTrial(grateOri,noiseOp):
    if grateOri<0:
        side=0
    else:
        side=1
    noise.opacity=noiseOp
    grate.ori=grateOri
    blank.draw()
    window.flip()
    core.wait(.2)
    grate.draw()
    noise.draw()
    window.flip()
    timer.reset()
    keys=event.waitKeys(keyList=['z','slash','9'],timeStamped=timer)
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
    if respInt==side:
        correct=1
        correct1.play()
        core.wait(0.1)
        correct2.play()
    else:
        correct=0
        error.play()
    core.wait(.5)
    return(respInt,rt,correct)
    return()

#######################################
### START EXPERIMENT ##################
#######################################

# staircase noise

side=[-1,1]*100
np.random.shuffle(side)

op=.7
last=0
for n in range(50):
    [resp,rt,correct]=doTrial(5*side[n],op)
    if correct==0:
        op=op-.01
        last=0
    elif last==1:
        op=op+.01
        last=0
    else: last=1
    print(op,last,correct)
        
    
    
del blank;
window.close()
core.quit()

