from psychopy import core, visual, event, sound
import random
import decimal
import sys
import numpy as np
import localLib


win = visual.Window(units="pix", size=(1024, 768), color="black", fullscr=True)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)
dot_size = 5


dot = visual.Circle(win, radius=5, units="pix", fillColor=[1, 1, 1])
core.wait(1)
dot.draw()
win.flip()

win.close()
core.quit()



