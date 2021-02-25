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


window=visual.Window(units= "pix", size =(640,320), rgb = "black", fullscr = False)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

#######################
# Trial Global Settings

s0=visual.TextStim(window, 
	text = "<<<<<<<", 
	pos = (0,0),
	color=[1,0,0],
	units='pix',
	height=64)
  
s1=visual.TextStim(window, 
	text = ">>>>>>>", 
	pos = (0,0),
	color=[0,1,0],
	units='pix',
	height=64)




def doTrial():

     frame=0;
     flag=True
     while flag:
          if (frame%2==0):
               s0.draw()
          else:
               s1.draw()
          window.flip()
          keys = event.getKeys()	
          flag = not "q" in keys and frame<600
          frame+=1 
     return()


############################################################
# Start Experiment 

doTrial()



##########################################################

core.quit()

