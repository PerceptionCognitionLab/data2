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
    image=os.path.join(__location__, 'set1-0.png'),
    pos=[-500,0],
	opacity=0.0)
c0.autoDraw=True

c1 = visual.ImageStim(window, 
    image=os.path.join(__location__, 'set1-0.png'),
    pos=[-250,0],
	opacity=0.0) 
c1.autoDraw=True

c2 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-0.png'),
	pos=[0,0],
	opacity=0.0)
c2.autoDraw=True

c3 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-0.png'),
	pos=[250,0],
	opacity=0.0)
c3.autoDraw=True

c4 = visual.ImageStim(window,
	image=os.path.join(__location__, 'set1-0.png'),
	pos=[500,0],
	opacity=0.0)
c4.autoDraw=True

numImage=['set1-1.png',
	  'set1-2.png',
	  'set1-3.png',
	  'set1-4.png',
	  'set1-5.png',
	  'set1-6.png',
	  'set1-7.png',
      'set1-8.png',
	  'set1-9.png',
	  'set1-0.png',]

r0=[0,1,2,3,4,5,6,7,8,9]
random.shuffle(r0)
r1 = r0[:]
random.shuffle(r1)
r2 = r1[:]
random.shuffle(r2)
r3 = r2[:]
random.shuffle(r3)
r4 = r3[:]
random.shuffle(r4)

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
        (rsvpO,rsvpI)=divmod(frame,30)
        if rsvpI==0:
            c0.image=numImage[r0[rsvpO%10]]
            c1.image=numImage[r1[rsvpO%10]]
            c2.image=numImage[r2[rsvpO%10]]
            c3.image=numImage[r3[rsvpO%10]]
            c4.image=numImage[r4[rsvpO%10]]            
        c0.opacity=(frame%3)/2
        c4.opacity=(frame%3)/2
        c1.opacity=(frame%5)/4
        c3.opacity=(frame%5)/4
        c2.opacity=(frame%7)/6
        window.flip()
        keys=event.getKeys()
        flag = not "q" in keys and frame <600
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
