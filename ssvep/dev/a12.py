from psychopy import core, visual, sound, event
from psychopy.hardware import keyboard
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
refreshRate=40
numPlaces=5 
numSlots=8
picRes=[100,110]
framesPerSlot =20

setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]

abortKey='9'
keysound=sound.Sound(225,secs=.07)
correct1=sound.Sound(400,secs=.1)
correct2=sound.Sound(600,secs=.2)
error=sound.Sound(50,secs=.4)

sounds = ["set1/Click2.wav"]
click = sound.Sound(sounds[0])

blank1FrameDur=4
fixFrameDur=20
blank2FrameDur=20

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
kb = keyboard.Keyboard()


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
    frameFlag=0
    
    for place in range(numPlaces):
        random.shuffle(digPrinted)
        digits.append(digPrinted[:])
    
    for slot in range(numSlots):
        for place in range(numPlaces):
            imArr[slot][place].image=digImg[int(digits[place][slot])]
            
    for place in range(numPlaces):
        imArr[crit][place].image=critImg[flank]
    imArr[crit][center].image=critImg[targ]

    window.flip()
    #timer.reset() 
    #kbFlag=True  
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
    kb.clock.reset()
    kb.clearEvents()
    kbFlag=True     
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())
        #TimeA = timer.getTime()             
        slot=frame//framesPerSlot
        for place in range(numPlaces):
            imArr[slot][place].opacity=(frame%freq[place])/(freq[place]-1)
            imArr[slot][place].draw()
        keys=kb.getKeys(['z','/'])
        myTimesB.append(timer.getTime())
        #TimeB = timer.getTime()
        #frameTime = timer.getTime() - TimeA        
        #onScreenFrame = TimeB - TimeA
        #myTimesA.append(TimeA)
        #myTimesB.append(TimeB)
        #if(onScreenFrame>0.016):
        #    frameFlag=frameFlag+1
        #if(frameTime>0.01):
        #    frameFlag=frameFlag+1
        if (len(keys)>0 & kbFlag):        
            keysound.play()
            resp=keys[0]
            kbFlag=False
        window.flip()
    if (resp.name==abortKey): 
        exit()
    for frame in [0,1]:
        blank.draw()
        window.flip()
    if resp.name=='z':
        respInt=0
    else: 
        respInt=1
    if targ==respInt:
        correct1.play()
        correct2.play()
    else:
        error.play()
    core.wait(.5)
    RT = resp.rt - ((crit * framesPerSlot)/refreshRate)  
    for a in range(numFrames):
        onScreenFrame = myTimesB[a] - myTimesA[a]
        if(onScreenFrame>0.005):
            frameFlag=frameFlag+1    
    return(respInt,RT,resp.rt,frameFlag)#myTimesA,myTimesB)


############################################################
# Start Experiment     
event.waitKeys()    


[resp,RT,keyrt,frameFlag]=doTrial(0,1,4)
print(resp,RT,keyrt,frameFlag)
[resp,RT,keyrt,frameFlag]=doTrial(0,0,4)
print(resp,RT,keyrt,frameFlag)
[resp,RT,keyrt,frameFlag]=doTrial(1,1,4)
print(resp,RT,keyrt,frameFlag)

#block=0
#for trial in range(1):
#        (flanker,target)=divmod(cond[order[trial]],2)
#        [resp,RT,keyrt,frameFlag,tA,tB]=doTrial(flanker,target,crit[trial])
#        rt = decimal.Decimal(RT).quantize(decimal.Decimal('1e-3'))
#        addData = (sessionID, block, trial,target,flanker,resp,rt,keyrt,crit[trial],frameFlag)
#        with open('timing.dat', 'w') as filehandle:
#            for i in range(len(tA)):
#                filehandle.write('%f %f\n' % (tA[i],tB[i]))
#        if useDB:
#            insertDatTable(insertTableStatement,addData,dbConf)
#        else:
#            print(addData)	
            
#with open('timing.dat', 'w') as filehandle:
#    for i in range(len(tA)):
#        filehandle.write('%f %f\n' % (tA[i],tB[i]))

##########################################################
hz=round(window.getActualFrameRate())
size=window.size
window.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)
    
core.quit()
