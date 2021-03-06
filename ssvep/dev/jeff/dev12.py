from psychopy import core, visual, sound, event
import os
import random
import sys
import decimal
import numpy as np
from PIL import Image
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = beta
expName='efRsvp1'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `flanker` INT(2) UNSIGNED NOT NULL,"
    "  `target` INT(2) UNSIGNED NOT NULL,"
    "  `resp` INT(1) NOT NULL,"
    "  `crit`  INT(5) UNSIGNED NOT NULL,"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")


insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `flanker`, `target`, `resp`, `crit`,`rt`, ``)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")


if useDB: 
	sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
    
    

#####################
# Settings  (GLOBAL SCOPE)
#####################
refreshRate=60
numPlaces=5 
numSlots=8
picRes=[100,110]
framesPerSlot =30

setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]

correct1=sound.Sound(400,secs=.1)
correct2=sound.Sound(600,secs=.2)
error=sound.Sound(50,secs=.4)

blank1FrameDur=6
fixFrameDur=30
blank2FrameDur=30

condRep=3

###################
# Start Up  (GLOBAL SCOPE)
###################
center=numPlaces//2
posX=[(a-center)*picRes[0] for a in range(numPlaces)]
screenRes= [a * b + 2 for a, b in zip(picRes,[numPlaces,1])]
window=visual.Window(units= "pix", size = screenRes, rgb = "black", fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)


#Make array
imArr=[]

for slot in range(numSlots):
    temp=[]
    for place in range(numPlaces):
        temp.append(visual.ImageStim(
                window,
                image="set1/set1-0.png",
                pos = (posX[place],0),
                units='pix'))
    imArr.append(temp)

digImg=[]
digPrinted=[]
for i in range(10):
    fname=setDir+'/'+setPre+str(i)+setPost
    digImg.append(Image.open(fname))
    digPrinted.append(str(i))


critImg=[]
critImg.append(Image.open(setDir+'/'+setPre+'AH-0.00'+setPost)) #A
critImg.append(Image.open(setDir+'/'+setPre+'AH-1.00'+setPost))


blank=visual.TextStim(window, text = "", pos = (0,0))
fix=[]
for place in range(numPlaces):
    fix.append(visual.ImageStim(
        window,
        image='set1/set1-+.png',
        pos=(posX[place],0),
        units='pix'))



###################################################
#Conditions
cond=np.repeat(range(4),condRep)
N=len(cond)
order=random.sample(range(N),N)
crit=np.random.randint(2,6,N)


##################################################
# Trial Function
##################################################
def doTrial(flank,targ,crit):
    numFrames=numSlots*framesPerSlot
    myTimesB=[]
    myTimesA=[]
    digits=[]
    onScreenTime=[]
    
    for place in range(numPlaces):
        random.shuffle(digPrinted)
        digits.append(digPrinted[:])
    
    for slot in range(numSlots):
        for place in range(numPlaces):
            imArr[slot][place].image=digImg[int(digits[place][slot])]
            
    for place in range(numPlaces):
        imArr[crit][place].image=critImg[flank]
    imArr[crit][center].image=critImg[targ]

  
    for frame in range(blank1FrameDur):
        blank.draw()
        window.flip()
    for frame in range(fixFrameDur):
        for place in range(numPlaces):
            fix[place].draw()
        window.flip()
    for frame in range(blank2FrameDur):
         blank.draw()
         window.flip()
    
    timer.reset()     
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())
        slot=frame//framesPerSlot
        for place in range(numPlaces):
            imArr[slot][place].opacity=(frame%freq[place])/(freq[place]-1)
            imArr[slot][place].draw()
        myTimesB.append(timer.getTime())
        window.flip()
    for frame in [0,1]:
        blank.draw()
        window.flip()
    keys=event.getKeys(['z','/'],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(timeStamped=timer)
    resp=keys[0]
    rt=keys[1]
    if resp=='z':
        respInt=0
    else:
        respInt=1
    for a in range(numFrames):
        onScreenTime.append(myTimesB[a] - myTimesA[a])
    return(respInt,rt,onScreenTime)


############################################################
# Start Experiment 

    
event.waitKeys()    

block=0
for trial in range(3):
        (flanker,target)=divmod(cond[order[trial]],2)
        [resp,RT,keyrt,onScreenTime]=doTrial(flanker,target,crit[trial])
        rt = decimal.Decimal(RT).quantize(decimal.Decimal('1e-3'))
        addData = (sessionID, block, trial,target,flanker,resp,rt,keyrt,crit[trial])
        if useDB:
            insertDatTable(insertTableStatement,addData,dbConf)
        else:
            print(addData)	

##########################################################
hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)
    
core.quit()
