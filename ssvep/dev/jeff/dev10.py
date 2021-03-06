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
picRes=[100,110]
setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]
framesPerSlot =30

abortKey='9'
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.1)
error=sound.Sound(300,secs=.2)

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
    
    for slot in range(numSlots):
        for place in range(numPlaces):
            imArr[slot][place].image=digImg[int(digits[place][slot])]
            
    for place in range(numPlaces):
        imArr[crit][place].image=critImg[flank]
    imArr[crit][center].image=critImg[targ]

    numFrames=numSlots*framesPerSlot

    window.flip()
    timer.reset()
    kb.clock.reset()
    kb.clearEvents()
    kbFlag=True
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())
        slot=frame//framesPerSlot
        for place in range(numPlaces):
            imArr[slot][place].opacity=(frame%freq[place])/(freq[place]-1)
            imArr[slot][place].draw()
        keys=kb.getKeys()
        if (len(keys)>0 & kbFlag):
            correct1.play()
            resp=keys[0]
            kbFlag=False
        myTimesB.append(timer.getTime())
        window.flip()

    return(myTimesA,myTimesB,resp)


############################################################
# Start Experiment 


event.waitKeys()
[checkA,checkB,key]=doTrial(0,0,3)
[checkC,checkD,key]=doTrial(0,0,3)
[checkE,checkF,key]=doTrial(1,0,3)


with open('timing.dat', 'w') as filehandle:
    for i in range(len(checkA)):
        filehandle.write('%d %f %f\n' % (1,checkA[i],checkB[i]))
    for i in range(len(checkC)):
        filehandle.write('%d %f %f\n' % (2,checkC[i],checkD[i]))
    for i in range(len(checkE)):
        filehandle.write('%d %f %f\n' % (3,checkE[i],checkF[i]))



##########################################################
window.close()
print(key.name,key.rt)

core.quit()


