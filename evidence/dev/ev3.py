from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os

win = visual.Window(units="pix", size=(1024, 768), color="black", fullscr=True)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

dot_size = 5

fix = visual.TextStim(win, text="+", height=30, color='white')

dot = visual.ElementArrayStim(
    win=win,
    nElements=1,
    sizes=dot_size,
    elementTex=None,
    elementMask="circle",
    units="pix",
)

show_fix=False
while not(event.getKeys(keyList=["9"])):
    keys = event.getKeys()

    if 'x' in keys:
        show_fix = ~show_fix

    if show_fix:
        fix.draw()
    else:
        dot.xys = np.random.uniform(-win.size[0]/2,win.size[0]/2,size=(1,2))
        dot.draw()

    win.flip()
    core.wait(0.5)
    win.flip()


win.close()
core.quit()








