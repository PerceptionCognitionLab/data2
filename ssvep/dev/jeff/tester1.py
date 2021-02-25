from psychopy import core, visual, sound, event
import random
import decimal
import numpy as np
from PIL import Image   
import os

refreshRate=60
numPlaces=5 
numSlots=8
picRes=[100,110]
framesPerSlot =30
numFrames=numSlots*framesPerSlot

setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]
center=numPlaces//2
posX=[(a-center)*picRes[0] for a in range(numPlaces)]


correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.1)
error=sound.Sound(300,secs=.2)

window=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(600,120),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

digImg=[]
fname=[]
for i in range(10):
    fname.append(setDir+'/'+setPre+str(i)+setPost)
    digImg.append(Image.open(fname[i]))

digImg.append(Image.open(setDir+'/'+setPre+'AH-0.00'+setPost))
digImg.append(Image.open(setDir+'/'+setPre+'AH-1.00'+setPost))




def doTrial(targ,flank,crit):
    blank=visual.TextStim(window, text = "", pos = (0,0))

    digits=[]
    a=list(range(10))
    for i in range(numSlots):
        random.shuffle(a)
        digits.append(a[-numPlaces:])

    for place in range(numPlaces):
        digits[crit][place]=10+flank
    digits[crit][center]=10+targ

    im=[]
    for frame in range(numFrames):
        [slot,local]=divmod(frame,framesPerSlot)
        if local==0:
            piece=[]
            for place in range(numPlaces):
                piece.append(visual.ImageStim(win=window,
                               pos=(posX[place],0),
                               image=digImg[digits[slot][place]],
                               opacity=(frame%freq[place])/(freq[place]-1)))
        else:
            for place in range(numPlaces):
                piece[place].opacity=(frame%freq[place])/(freq[place]-1)       
        im.append(visual.BufferImageStim(win=window,stim=piece,rect=[-.3,.1,.3,-.1]))


    myTimesB=[]
    myTimesA=[]
    timer.reset()
    for frame in range(numFrames):
        myTimesA.append(timer.getTime())    
        im[frame].draw()
        myTimesB.append(timer.getTime())
        window.flip()
    for frame in [0,1]:
        blank.draw()
        window.flip()
    keys=event.getKeys(keyList=['q','p'],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=['q','p'],timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
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
    core.wait(.5)
    frameSkipped=0
    for a in range(numFrames):
        if myTimesB[a] - myTimesA[a]>(1/refreshRate-.001):
            frameSkipped+=1
    del(im)
    return(respInt,rt,frameSkipped)





for t in range(3):
    out=doTrial(targ=t%2,flank=0,crit=3)
    print(out)


window.close()
core.quit()

