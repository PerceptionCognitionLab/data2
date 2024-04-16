from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os
import time

scale=400

window=visual.Window(units= "pix", 
                     size=(2*scale,2*scale),
                     color='black',
                     fullscr = True)

message=visual.TextStim(window,text="Hello World",
                        pos=(0,0),
                        height=20)


message_2 = visual.TextStim(window,text="Bye World",
                            pos=(0,0),
                            height=20)


message.draw()
window.flip()
core.wait(1)
message_2.draw()
window.flip()
core.wait(1)
window.close()

core.quit()
