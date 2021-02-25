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

  
stringNum=[]
for i in range(10):
    stringNum.append('set1/set1-'+str(i)+'.png')



def doTrial():
    digits=[]
    for j in range(8):
        digits.append(random.sample(stringNum,3))
    
    fa= []
    for i in range(8):
        temp=[]
        for j in range(3):
            temp.append(Image.open(digits[i][j]))
        fa.append(temp)
    
    frame=0;
    
    flag=True
    while flag:
        v[0].image=fa[0][0]
        v[1].image=fa[1][1]
        v[2].image=fa[2][2]        
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

#window.getMovieFrame(buffer='front') 
doTrial()
#window.saveMovieFrames('dev4.mp4')


##########################################################
window.close()
core.quit()

