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

stimuli = ['x', 'm']
text = visual.TextStim(win)

def run_trial(stimulus):
    text.setText(stimulus)
    text.draw()
    win.flip()
    timer.reset()


for i in range(10):  
    stimulus = random.choice(stimuli)  
    
    core.wait(0.5)  
    run_trial(stimulus)
    
    keys = event.waitKeys(keyList=['x', 'm', 'escape'])
    
    if 'escape' in keys:
        print("Experiment aborted by the user.")
        break  
    response_time = timer.getTime()  
    print(f"Stimulus:{stimulus}, Response: {keys[0]}, Response Time: {response_time}")



win.close()
core.quit()




