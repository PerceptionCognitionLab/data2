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
window=visual.Window(units= "pix", size =(1280,640), rgb = "black", fullscr = False,)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

__location__ = os.path.realpath(
   os.path.join(os.getcwd(), os.path.dirname(__file__)))

#######################
# Trial Global Settings


posVals=[-200,-100,0,100,200]
place=[]

for i in range(5):
    place.append(visual.ImageStim(window, 
                                  pos = (posVals[i],0),
                                  units='pix', image='set1-0.png',
                                  opacity=0.0))
for x in place:
    x.autoDraw=True
	

def fileName(strg):
    return('set1-'+strg+'.png')
    
order_outerLeft=[]
for i in range(10):
  order_outerLeft.append(str(i))
random.shuffle(order_outerLeft)
order_innerLeft = order_outerLeft[:]
random.shuffle(order_innerLeft)
order_Center = order_innerLeft[:]
random.shuffle(order_Center)
order_innerRight = order_Center[:]
random.shuffle(order_innerRight)
order_outerRight = order_innerRight[:]
random.shuffle(order_outerRight)

criticalNames=['AH-0.00','AH-1.00']
freq=(4,3,2,3,4)


datos=open("Flickr01c"+"_"+time.strftime("%Y-%m-%d")+".csv", 'w')
datos.write("Frame, Duration,\n")
datos.close


#######################
# Trial development
text1=visual.TextStim(window, text="Press Q to exit", pos = (0,100))

def doTrial(outL,innL,targ,innR,outR):
    init_time = time.time()
    digits=[]
    for i in range(5):
        place[i].opacity=1.0
    for j in range(8):
        digits.append((order_outerLeft[j],order_innerLeft[j],order_Center[j],
                      order_innerRight[j],order_outerRight[j]))
    digits[4]=[criticalNames[outL],criticalNames[innL],criticalNames[targ],
               criticalNames[innR],criticalNames[outR]]
    frame=0;
    flag=True
    window.flip()
    while flag:
        window.getMovieFrame(buffer='front') 
        frame_init= time.time()
        (let,letFrame)=divmod(frame,30)
        if letFrame==0:
            count30F_init = time.time()
            for i in range(5):
                place[i].image=fileName(digits[let][i])
        for i in range(5):            
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

text=visual.TextStim(window, text = "Welcome\n Press any key to begin\n Press q to exit", pos = (0,0))
window.getMovieFrame(buffer='front') 
text.draw()
window.flip()
event.waitKeys()
doTrial(1,1,0,1,1)
window.saveMovieFrames('f01_d.mp4')

window.close()
core.quit()
