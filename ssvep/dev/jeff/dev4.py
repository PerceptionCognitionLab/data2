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


window=visual.Window(units= "pix", size =(350,120), rgb = "black", fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

#######################
# Trial Global Settings


s0=visual.ImageStim(window, 
	pos = (-100,0),
	units='pix')
	
s0.autoDraw=True
	
  
s1=visual.ImageStim(window, 
	pos = (0,0),
	units='pix')
	
s1.autoDraw=True


s2=visual.ImageStim(window, 
	pos = (100,0),
	units='pix')
	
s2.autoDraw=True


v=[s0,s1,s2]

myNumbers=range(8)
myFileNames=[]
for i in myNumbers:
    myFileNames.append('set1/set1-'+str(myNumbers[i])+'.png')
    


def doTrial():

    frame=0;
    flag=True
    v[0].image='set1/set1-A.png'
    v[1].image='set1/set1-H.png'
    v[2].image='set1/set1-A.png'
    
    while flag:
        v[0].opacity=(frame%4)/3
        v[1].opacity=(frame%3)/2
        v[2].opacity=(frame%4)/3
        window.getMovieFrame(buffer='front') 
        window.flip()
        keys = event.getKeys()
        flag = not "q" in keys and frame<240
        frame+=1 
    return()


############################################################
# Start Experiment 

window.getMovieFrame(buffer='front') 
doTrial()
window.saveMovieFrames('dev4.mp4')


##########################################################
window.close()
core.quit()

