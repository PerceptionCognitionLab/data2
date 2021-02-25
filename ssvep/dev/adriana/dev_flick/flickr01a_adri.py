from psychopy import core, visual, sound, event
import os
import random
import sys
import decimal
import numpy as np
from numpy import cumsum
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
c0 = visual.ImageStim(window, 
    image=os.path.join(__location__, 'set1-1.png'),
    pos=[-500,0],
	opacity=0.0)
c0.autoDraw=True

c1 = visual.ImageStim(window, 
    image=os.path.join(__location__, 'set1-2.png'),
    pos=[-250,0],
	opacity=0.0) 
c1.autoDraw=True

c2 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-3.png'),
	pos=[0,0],
	opacity=0.0)
c2.autoDraw=True

c3 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-4.png'),
	pos=[250,0],
	opacity=0.0)
c3.autoDraw=True

c4 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-5.png'),
	pos=[500,0],
	opacity=0.0)
c4.autoDraw=True


#######################
# Trial development
text1=visual.TextStim(window, text="Press Q to exit", pos = (0,200))

def doTrial():
    frame=0;
    flag=True
    c0.opacity=1.0
    c1.opacity=1.0
    c2.opacity=1.0
    c3.opacity=1.0
    c4.opacity=1.0
    text1.autoDraw=True
    while flag:
        [val,res] = divmod(frame,30)
        c0.opacity=(frame%3)/2
        c4.opacity=(frame%3)/2
        c1.opacity=(frame%4)/3
        c3.opacity=(frame%4)/3
        c2.opacity=(frame%5)/4
        window.flip()
        keys=event.getKeys()
        flag = not "q" in keys and frame <400
        frame+=1
    return(print(val))


############################################################
# Start Experiment 

text=visual.TextStim(window, text = "Welcome\n Press any key to begin\n Press q to exit", pos = (0,0))
text.draw()
window.flip()
event.waitKeys()

doTrial()

window.close()
core.quit()
