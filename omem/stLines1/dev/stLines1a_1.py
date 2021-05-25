from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os

##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=False
dbConf = exp
expName='octo2a'
abortKey='q'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `stimGlobA` INT(3) UNSIGNED NOT NULL,"
    "  `stimGLobB` INT(1) UNSIGNED NOT NULL,"
    "  `weightA` DECIMAL(4.3) NOT NULL,"
    "  `correctResp` CHAR(1),"
    "  `resp` CHAR(1),"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `stimGlobA`, `StimGlobB`, `weightA`, `correctResp`,`resp`,`rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

if useDB:
    sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1     
      
########################################
# GLOBAL SETTINGS  #####################
########################################
scale=400
window=visual.Window(units= "pix", allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1], fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)

########################################
# Functions  ###########################
########################################
def length(p,nLen):
    out=np.empty((nLen,2))
    for i in range(nLen-1):
        out[i]=p[i]
    return(out)

def readPoly(fname,scale):
    octoIN=np.loadtxt(fname,dtype=float)
    numPoly=int(max(octoIN[:,0]))
    numPoints=int(np.shape(octoIN)[0]/numPoly)
    octoIN=np.reshape(octoIN[:,1:3],(numPoly,numPoints,2))
    return(scale*(octoIN-.5))

def slideshow(p,map="None"):
    im=visual.Line(window, start=[-p[:],0],end=[p[:],0])
    numShow=stim.shape[0]
    if (map=="None"): 
        map=np.repeat("",numShow)
    blank=visual.TextStim(window,"")
    ans=visual.TextStim(window,text=map[0],
                        pos=(0,scale/2),
                        height=40,bold=True,
                        anchorVert="bottom")
    for i in range(numShow):
        ans.text=map[i]
        im.draw()
        ans.draw()
        window.flip()
        event.waitKeys()
        blank.draw()
        window.flip()
        
        
def trialAbsId(p,map):
    im=visual.Line(window, start=[-p[:],0],end=[p[:],0])                               
    feedback=visual.TextStim(window,text=map,
                        pos=(0,scale/2),
                        height=20,bold=True,
                        anchorVert="bottom")
    blank=visual.TextStim(window,"")
    timer.reset()
    im.draw()
    window.flip()
    keys=event.waitKeys(keyList=('1','2','3','4','5','6','7','8',abortKey),
                        timeStamped=timer)
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
        
########################################
# VARIABLES   ##########################
########################################
end=400
nLen = 10
p=np.linspace(50,end,nLen)
#m=morph(octo[0,:,:],octo[1,:,:],p)

fname="/home/exp/specl-exp/data2/omem/dev/s1.octo"
octo=readPoly(fname,scale)
stimChoice=np.random.choice(np.shape(octo)[0],2,replace=False)
stimChoice=np.array([23,41])
stim=octo[stimChoice,:,:]
ans=np.arange(1,9,dtype="int")
map=[]
for i in range(8):
    map.append(str(ans[i]))
slideshow(p,map)

########################################
# RUN EXPERIMENT########################
########################################
ans=np.arange(1,nLen+1,dtype="int")
map=[]
for i in range(nLen):
    map.append(str(ans[i]))
slideshow(p,map)

numReps=30
numTrials=numReps*8
numTrialsPerBlock=80
stimIndex=np.repeat(range(8),numReps)
random.shuffle(stimIndex)

for n in range(numTrials):
    (b,t)=divmod(n,numTrialsPerBlock)
    if t==0 and b>0:
        takeABreak()
    out=trialAbsId(2,2)
    rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
    weight=decimal.Decimal(p[stimIndex[n]]).quantize(decimal.Decimal('1e-3'))
    addData = (sessionID, b, t, 
               stimChoice[0], stimChoice[1],weight, 
               map[stimIndex[n]],out[0], rt)
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