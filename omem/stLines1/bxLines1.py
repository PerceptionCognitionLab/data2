from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os

################################################
######### DESCRIPTION
#########
######### Task: Absolute identification task
######### Stimuli: Line lengths within a box
######### Conditions: 2 Boz sizes (expCondition)
######### Specifics: No mask and fixated location of lines
################################################

##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = exp
expName = 'bxLines1'
expCondition = 1 #"1" for full size; "2" for half sizes
base = 100   #Length of the reference line (Line #1)
rate = 1.5   #Increment rate between lines
nLen = 7     #Number of line lengths included

abortKey='q'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `length` DECIMAL(5,3),"
    "  `correctResp` CHAR(1),"
    "  `resp` CHAR(1),"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `length`, `correctResp`,`resp`,`rt`)"
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
                     size=(1680,1050),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

## Feedback sounds
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)

## Setting up lines
def linelength(base, rate, n):
    l = list(range(n))
    length = base*pow(rate,np.array(l))
    return(length)

length = linelength(base,rate,nLen)
endpoint = np.array(length)/(2*expCondition)

## Setting up box
wBox = 1400/expCondition
hBox = 800/expCondition


########################################
# MAIN FUNCTIONS  ######################
########################################
def slideshow(endpoint,map="None"): 
    if (map=="None"): 
        map=np.repeat("",10)
    box = visual.Rect(window, width=wBox, height=hBox)
    blank=visual.TextStim(window,"")
    ans=visual.TextStim(window,text=map[0],
                        pos=(0,100),
                        height=40,bold=True,
                        anchorVert="bottom")
    for i in range(nLen):
        im=visual.Line(window, start=[-endpoint[i],0],
                       end=[endpoint[i],0])  
        ans.text=map[i]        
        im.draw()
        ans.draw()
        box.draw()
        window.flip()
        box.draw()
        event.waitKeys()
        blank.draw()
        window.flip()
        
        
def trialAbsId(endpoint,map):
    box=visual.Rect(window,width=wBox,height=hBox)
    im=visual.Line(window, start=[-endpoint,0],
                   end=[endpoint,0])    
    feedback=visual.TextStim(window,text=map,
                        pos=(0,100),
                        height=20,bold=True,
                        anchorVert="bottom")
    blank=visual.TextStim(window,"")
    timer.reset()
    im.draw()
    box.draw()
    window.flip()
    box.draw()
    keys=event.waitKeys(keyList=('1','2','3','4','5','6','7',
                                 abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        window.close()
        core.quit()   
    if (resp==map):
        correct1.play()
        correct2.play()
        core.wait(.5)
    else:
        feedback.text="Error. Your Answer: "+resp+".  Correct Answer: "+map
        im.draw()
        feedback.draw()
        window.flip()        
        box.draw()
        event.waitKeys()
    blank.draw()
    window.flip()
    core.wait(.5)
    return(resp,rt)
    
def takeABreak():
        message=visual.TextStim(window,"Take A Break....Hit Any Key To Resume")
        message.draw()
        window.flip()
        event.waitKeys()
        
ans=np.arange(1,9,dtype="int")
map=[]
for i in range(nLen):
    map.append(str(ans[i]))
slideshow(endpoint,map)

numReps=30
numTrials=numReps*8
numTrialsPerBlock=80
stimIndex=np.repeat(range(nLen),numReps)
random.shuffle(stimIndex)

for n in range(numTrials):
    (b,t)=divmod(n,numTrialsPerBlock)
    if t==0 and b>0:
        takeABreak()
    out=trialAbsId(endpoint[stimIndex[n]],map[stimIndex[n]])
    rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
    addData = (sessionID, b, t, length[stimIndex[n]], map[stimIndex[n]], out[0], rt)
    if useDB:
        insertDatTable(insertTableStatement,addData,dbConf)
    else:
        print(addData)	

hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)


core.quit()
