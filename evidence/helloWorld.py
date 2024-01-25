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


                        

timer = core.Clock()
#seed = random.randrange(1e6)
#rng = random.Random(seed)

#hz=round(win.getActualFrameRate())
#size=win.size
#win.close()
#if useDB:
#	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

#print(hz)

def trial():
	message=visual.TextStim(window,text="Hello World",
                        pos=(0,0),
                        height=20)

	c=visual.TextStim(window,text="+",
                        pos=(0,0),
                        height=20)
	dot = visual.Circle(window, radius=5, units="pix", fillColor=[1, 1, 1])
	dot.draw()
	window.flip()
	core.wait(1)
	message.draw()
	window.flip()
	timer.reset()
	present=timer.getTime
	response=event.waitKeys()
	rt=timer.getTime()
	return(rt,response,present)


[rt,response,present]=trial()
all_resp=[]
for i in range(1):
	trial()
	cresp=(response,rt)
	all_resp.append(cresp)


window.close()
print("response",all_resp)


core.quit()




