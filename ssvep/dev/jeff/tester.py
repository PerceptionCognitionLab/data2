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
numIm=numSlots*framesPerSlot

setDir = "/home/exp/specl-exp/data2/ssvep/dev/set1"
setPre = "set1-"
setPost = ".png"
freq=[2,4,3,4,2]
center=numPlaces//2
posX=[(a-center)*picRes[0] for a in range(numPlaces)]

window=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(600,120),
                     color=[-1,-1,-1],
                     fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

digImg=[]
fname=[]
for i in range(10):
    fname.append(setDir+'/'+setPre+str(i)+setPost)
    digImg.append(Image.open(fname[i]))


digits=[]
a=list(range(10))
for i in range(numSlots):
    random.shuffle(a)
    digits.append(a[-numPlaces:])




def doTrial():
    im=[]
    for frame in range(240):
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
        im.append(visual.BufferImageStim(win=window,stim=piece))


    myTimesB=[]
    myTimesA=[]
    for frame in range(240):
        myTimesA.append(timer.getTime())    
        im[frame].draw()
        myTimesB.append(timer.getTime())
        window.flip()
    del(im)
    return(myTimesA,myTimesB)


timer.reset()



timeFile='timing.dat'
if os.path.exists(timeFile):
    os.remove(timeFile)

for t in range(3):
    [tA,tB]=doTrial()
    with open(timeFile, 'a') as filehandle:
        for i in range(len(tA)):
            filehandle.write('%d %f %f\n' % (t,tA[i],tB[i]))


window.close()
core.quit()

