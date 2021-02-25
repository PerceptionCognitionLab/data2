from psychopy import core, visual, sound, event
import os
import random
import sys
import decimal
import time
import numpy as np


SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)



#####################
# Experiment Settings
#####################


window=visual.Window(units= "pix", size =(350,120), rgb = "black", fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

#######################
# Trial Global Settings

posVals=[-100,0,100]
place=[]

for i in range(3):
    place.append(visual.ImageStim(window, 
                                  pos = (posVals[i],0),
                                  units='pix',
                                  image='set1-0.png'))

for x in place:
    x.autoDraw=True
	

def fileName(strg):
    return('set1-'+strg+'.png')
    

stringNum=[]
for i in range(10):
    stringNum.append(str(i))

criticalNames=['AH-0.00','AH-1.00']
freq=(4,3,2)

datos=open("Erik10"+"_"+time.strftime("%Y-%m-%d")+".csv", 'w')
datos.write("Frame, Duration,\n")
datos.close

def doTrial(flank,targ):
    init_time = time.time()
    digits=[]
    for j in range(8):
        digits.append(random.sample(stringNum,3))
    digits[5]=[criticalNames[flank],criticalNames[targ],criticalNames[flank]]
    frame=0;
    flag=True
    window.flip()
    while flag:
        frame_init= time.time()
        (let,letFrame)=divmod(frame,30)
        if letFrame==0:
            count30F_init = time.time()
            for i in range(3):
                place[i].image=fileName(digits[let][i])
        for i in range(3):
            place[i].opacity=(frame%freq[i])/(freq[i]-1)
        window.flip()
        keys = event.getKeys()
        flag = not "q" in keys and frame<239
        frame+=1 
        frame_end= time.time() - frame_init
        datos.write(str(frame)+","+str(frame_end)+","+"\n")
        print('Frame',frame, 'duration =', frame_end)
    count30F_end = time.time() - count30F_init
    print('Seconds in 30 Frames', count30F_end)
    end_time = time.time() - init_time
    print('doTrial total duration', end_time)
    return()

############################################################
# Start Experiment 


event.waitKeys()
doTrial(0,0)
event.waitKeys()
doTrial(1,0)
event.waitKeys()

##########################################################
window.close()
core.quit()

