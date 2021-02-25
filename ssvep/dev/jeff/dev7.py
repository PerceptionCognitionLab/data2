from psychopy import core, visual, sound, event
import os
import random
import sys
import decimal
import numpy as np


SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)



#####################
# Experiment Settings
#####################


window=visual.Window(units= "pix", size =(350,120), rgb = "black", fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)
window.recordFrameIntervals = True

#######################
# Trial Global Settings

posVals=[-100,0,100]

imArr=[]

for i in range(8):
    temp=[]
    for j in range(3):
        temp.append(visual.ImageStim(
                window,
                pos = (posVals[j],0),
                units='pix',
                image='set1/set1-0.png'))
    imArr.append(temp)



	
stringNum=[]
for i in range(10):
    stringNum.append('set1/set1-'+str(i)+'.png')

criticalNames=['set1/set1-AH-0.00.png','set1/set1-AH-1.00.png']
freq=(4,3,4)



def doTrial(flank,targ):
    timer.reset()
    myTimesB=[]
    myTimesA=[]
    digits=[]
    for j in range(8):
        digits.append(random.sample(stringNum,3))    

    for i in range(8):
        for j in range(3):
            imArr[i][j].image=digits[i][j]

    frame=0;
    flag=True
    window.flip()
    while flag:
        myTimesA.append(timer.getTime())
        slot=frame//30
        for j in range(3):
            imArr[slot][j].opacity=(frame%freq[j])/(freq[j]-1)
            imArr[slot][j].draw()
        myTimesB.append(timer.getTime())
        window.flip()
        keys = event.getKeys()
        flag = not "q" in keys and frame<239
        frame+=1
    return(myTimesA,myTimesB)


############################################################
# Start Experiment 


event.waitKeys()
[checkA,checkB]=doTrial(0,0)


with open('timing.dat', 'w') as filehandle:
    for i in range(len(checkA)):
        filehandle.write('%f %f\n' % (checkA[i],checkB[i]))

##########################################################
window.close()
core.quit()
