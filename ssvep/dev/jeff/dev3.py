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

#######################
# Trial Global Settings

s0=visual.ImageStim(window, 
	image='set1/set1-AH-0.00.png', 
	pos = (-100,0),
	units='pix')
	
s0.autoDraw=True
	

  
s1=visual.ImageStim(window, 
	image='set1/set1-AH-0.50.png', 
	pos = (0,0),
	units='pix')
	
s1.autoDraw=True


s2=visual.ImageStim(window, 
	image='set1/set1-AH-0.00.png', 
	pos = (100,0),
	units='pix')
	
s2.autoDraw=True

myImage=['set1/set1-AH-0.00.png',
         'set1/set1-AH-0.50.png',
         'set1/set1-AH-1.00.png']


def doTrial():

    frame=0;
    flag=True
    while flag:
        (rsvpO,rsvpI)=divmod(frame,30)
        if rsvpI==0:
            s1.image=myImage[rsvpO%3]
        s0.opacity=(frame%3)/2
        s1.opacity=(frame%4)/3
        s2.opacity=(frame%5)/4
        window.flip()
        keys = event.getKeys()
        flag = not "q" in keys and frame<240
        frame+=1 
    return()


############################################################
# Start Experiment 

doTrial()



##########################################################
window.close()
core.quit()

