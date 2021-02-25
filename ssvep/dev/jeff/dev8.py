from psychopy import core, visual, sound, event
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
setDir = "/home/exp/specl-exp/data2/ssvep/dev/jeff/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]
framesPerSlot =30


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
for i in range(10):
    fname=setDir+'/'+setPre+str(i)+setPost
    digImg.append(Image.open(fname))


critImg=[]
critImg.append(Image.open(setDir+'/'+setPre+'AH-0.00'+setPost))
critImg.append(Image.open(setDir+'/'+setPre+'AH-1.00'+setPost))

    


##################################################
# Trial Function
##################################################

def doTrial(flank,targ,crit):
    timer.reset()
    myTimesB=[]
    myTimesA=[]
    digits=[]
    for slot in range(numSlots):
        digits.append(random.sample(range(10),numPlaces))    

    for slot in range(numSlots):
        for place in range(numPlaces):
            imArr[slot][place].image=digImg[digits[slot][place]]
            
    for place in range(numPlaces):
        imArr[crit][place].image=critImg[flank]
    imArr[crit][center].image=critImg[targ]

    window.flip()
    numFrames=numSlots*framesPerSlot
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())
        slot=frame//framesPerSlot
        for place in range(numPlaces):
            imArr[slot][place].opacity=(frame%freq[place])/(freq[place]-1)
            imArr[slot][place].draw()
        myTimesB.append(timer.getTime())
        window.flip()
    return(myTimesA,myTimesB)


############################################################
# Start Experiment 


event.waitKeys()
[checkA,checkB]=doTrial(0,0,4)


with open('timing.dat', 'w') as filehandle:
    for i in range(len(checkA)):
        filehandle.write('%f %f\n' % (checkA[i],checkB[i]))

##########################################################
window.close()
core.quit()
