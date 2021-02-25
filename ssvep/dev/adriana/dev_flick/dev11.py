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



#####################
# Settings  (GLOBAL SCOPE)
#####################
numPlaces=5 
numSlots=8
numPreSlots=2
totalSlots = numSlots + numPreSlots
picRes=[100,110]
setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]

framesPerSlot =30
BlankScreen = int(30/5)
numFrames_pre = numPreSlots*framesPerSlot+BlankScreen
numFrames_main = numSlots*framesPerSlot

keypress=sound.Sound(225,secs=.07)
correct=sound.Sound(500,secs=.2)
error=sound.Sound(50,secs=.2)

abortKey='9'
respKey = ["z"]
RespKey = []
RespKey.append('z')
RespKey.append('|')

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

for slot in range(totalSlots):
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

fixImg=[]
fixImg.append(Image.open(setDir+'/'+setPre+'+'+setPost)) 
fixImg.append(Image.open(setDir+'/'+setPre+'empty'+setPost)) 
##################################################
# Trial Function
##################################################

def doTrial(flank,targ,crit):
    myTimesB=[]
    myTimesA=[]
    digits=[]
    
    for place in range(numPlaces):
        random.shuffle(digPrinted)
        digits.append(digPrinted[:])
   
    for slot in range(totalSlots):
        for place in range(numPlaces):
            if(slot < numPreSlots):
                imArr[slot][place].image=fixImg[slot]
            if(slot >= numPreSlots):
                s = slot-numPreSlots
                imArr[slot][place].image=digImg[int(digits[place][s])]        
            
    for place in range(numPlaces):
        imArr[crit][place].image=critImg[flank]
    imArr[crit][center].image=critImg[targ]

    window.flip()
    for frame in range(numFrames_pre):
        pre = frame//BlankScreen
        for place in range(numPlaces):         
            if(pre<1):
                imArr[1][place].draw()        
            if(pre>=1):
                slot=(frame-BlankScreen)//framesPerSlot
                imArr[slot][place].draw()            
        window.flip()
        
    timer.reset()        
    kb.clock.reset()
    kb.clearEvents()
    kbFlag=True         
    for frame in range(numFrames_main):
        myTimesA.append(timer.getTime())
        slot=(frame//framesPerSlot)+numPreSlots
        for place in range(numPlaces):
            imArr[slot][place].opacity=(frame%freq[place])/(freq[place]-1)
            imArr[slot][place].draw()
        keys=kb.getKeys()
        if (len(keys)>0 & kbFlag):
            print(keys)
            keypress.play()
            resp=keys[0]
            kbFlag=False            
        myTimesB.append(timer.getTime())
        window.flip()    
    return(myTimesA,myTimesB,resp)


############################################################
# Start Experiment 
event.waitKeys()
[checkA,checkB,key]=doTrial(0,0,3)


with open('timing.dat', 'w') as filehandle:
    for i in range(len(checkA)):
        filehandle.write('%f %f\n' % (checkA[i],checkB[i]))

##########################################################
window.close()
print(key.name,key.rt)

core.quit()


