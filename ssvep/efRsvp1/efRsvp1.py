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

useDB=True
dbConf = exp
expName='efRsvp1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(5) UNSIGNED NOT NULL,"
    "  `trial` INT(10) UNSIGNED NOT NULL,"
    "  `flanker` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `resp` INT(1) NOT NULL,"
    "  `crit`  INT(1) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"    
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `flanker`, `target`, `resp`, `crit`,`rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
########################################
# GLOBAL SETTINGS  #####################
########################################
window=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(600,120),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)


########################################
# CONDITIONS AND BLOCKS  ###############
########################################
nBlocks=2
nTrials=3
Rep=3
cond=np.repeat(range(4),Rep)
N=len(cond)
order=random.sample(range(N),N)
crit=np.random.randint(2,6,N)


###############################
# START UP   ##################
###############################
refreshRate=60
numPlaces=5 
numSlots=8
picRes=[100,110]
framesPerSlot =30
numFrames=numSlots*framesPerSlot
fBlank1 = 6
fBlank2 = 30
fFix = 30
preRSVP = fBlank1+fBlank2+fFix

setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[3,3,2,3,3]
center=numPlaces//2
posX=[(a-center)*picRes[0] for a in range(numPlaces)]

keysound=sound.Sound(225,secs=.07)
correct1=sound.Sound(400,secs=.1)
correct2=sound.Sound(600,secs=.2)
error=sound.Sound(50,secs=.4)
quitting=sound.Sound(70,secs=.2)


abortKey='9'
################################
# CREATE IMAGES  ###############
################################
digImg=[]
fname=[]
for i in range(10):
    fname.append(setDir+'/'+setPre+str(i)+setPost)
    digImg.append(Image.open(fname[i]))

digImg.append(Image.open(setDir+'/'+setPre+'AH-0.00'+setPost))
digImg.append(Image.open(setDir+'/'+setPre+'AH-1.00'+setPost))
digImg.append(Image.open(setDir+'/'+setPre+'+'+setPost))


Xfix=[]
for place in range(numPlaces):
    Xfix.append(visual.ImageStim(win=window,
                               pos=(posX[place],0),
                               image=digImg[12],
                               opacity=1.0))
fix = visual.BufferImageStim(win=window,stim=Xfix,rect=[-.3,.1,.3,-.1])


Blank=visual.TextStim(window, text = "", pos = (0,0))
Welcome=visual.TextStim(window, text = "Identify the letter that appears at the center of the screen\n\n\n Press the 'q' key for A\n\n Press the 'p' key for H\n\n\n\n Press any key to begin", pos = (0,0))
Pause=visual.TextStim(window, text = "Press any key to continue to the next block of trials", pos = (0,0))
Reminder=visual.TextStim(window, text = "Please enter your response", pos = (0,0))
Quit=visual.TextStim(window, text = "Quiting experiment...", pos = (0,0))
Thnx=visual.TextStim(window, text = "Thank you for your time!\n\n You may call the experimenter now!", pos = (0,0))

####################################
##  TRIAL SET UP   #################
####################################
def doTrial(targ,flank,crit):

    digits=[]
    a=list(range(10))
    for i in range(numPlaces):
        random.shuffle(a)
        digits.append(a[-numSlots:])

    for place in range(numPlaces):
        digits[place][crit]=10+flank
    digits[center][crit]=10+targ

    im=[]
    for frame in range(numFrames):
        [slot,local]=divmod(frame,framesPerSlot)
        if local==0:
            piece=[]
            for place in range(numPlaces):
                piece.append(visual.ImageStim(win=window,
                               pos=(posX[place],0),
                               image=digImg[digits[place][slot]],
                               opacity=(frame%freq[place])/(freq[place]-1)))
        else:
            for place in range(numPlaces):
                piece[place].opacity=(frame%freq[place])/(freq[place]-1)       
        im.append(visual.BufferImageStim(win=window,stim=piece,rect=[-.3,.1,.3,-.1]))

    for a in range(preRSVP):
        if(a//fBlank1==0):
            Blank.draw()            
            window.flip()
        elif(a//(fBlank1+fFix)==0):
            fix.draw()
            window.flip()
        else:
            Blank.draw()
            window.flip()

    myTimesB=[]
    myTimesA=[]
    timer.reset()
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())    
        im[frame].draw()
        myTimesB.append(timer.getTime())
        window.flip()
    for frame in [0,1]:
        Blank.draw()
        window.flip()
    keys=event.getKeys(keyList=['q','p',abortKey],timeStamped=timer)
    if len(keys)==0:
        Reminder.draw()
        window.flip()       
        keys=event.waitKeys(keyList=['q','p',abortKey],timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey: 
        for i in range(framesPerSlot):
            Quit.draw()
            window.flip()
        exit()
    if resp=='q':
        respInt=0
    else:
        respInt=1  
    if (respInt==targ):
        correct1.play()
        core.wait(0.1)
        correct2.play()
    else: 
        error.play()
    frameSkipped=0
    for a in range(numFrames):
        if myTimesB[a] - myTimesA[a]>(1/refreshRate-.001):
            frameSkipped+=1
    del(im)        
       
    core.wait(.5)
    return(respInt,rt,frameSkipped)


#######################################
### START EXPERIMENT ##################
#######################################
Welcome.draw()
window.flip()
event.waitKeys()

for block in range(nBlocks):
    BlockID = block
    for trial in range(nTrials):
        (target,flanker)=divmod(cond[order[trial]],2)
        [resp,RT,frameFlag]=doTrial(target,flanker,crit[trial])
        rt = decimal.Decimal(RT).quantize(decimal.Decimal('1e-3'))
        addData = (sessionID, BlockID, trial,flanker,target,resp,crit[trial],rt)        
        if useDB:
            insertDatTable(insertTableStatement,addData,dbConf)
        else:
            print(addData)	
    Pause.draw()
    window.flip()
    event.waitKeys()


Thnx.draw()
window.flip()
event.waitKeys()

########################################
# End Experiment
#######################################3
hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
        stopExp(sessionID,hz,size[0],size[1],seed,dbConf)
core.quit()