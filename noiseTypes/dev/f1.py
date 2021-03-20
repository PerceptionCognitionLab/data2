from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np
from PIL import Image   
import os


resX=200
resY=200



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

    



def doTrial():

    blank=visual.TextStim(win=window,text="")
    grate= visual.GratingStim(win=window,sf=.05,size=300,mask="gauss",
                              ori=1,opacity=.3)
    noise=visual.NoiseStim(win=window,size=(300,300),noiseType="uniform",
                           noiseElementSize=2,opacity=0)
    blank.draw()
    window.flip()
    core.wait(.2)
    grate.draw()
    noise.draw()
    window.flip()
    core.wait(3)
    return()

#######################################
### START EXPERIMENT ##################
#######################################

doTrial()

window.close()
core.quit()

