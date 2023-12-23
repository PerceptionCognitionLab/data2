from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os
import localLib



expName="dev.ev4"
runMode=False


[fptr,sub]=localLib.startExp(expName,runMode)

win = visual.Window(units="pix", size=(1024, 768), color="black", fullscr=True)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)
dot_size = 5

fix = visual.TextStim(win, text="+", height=30, color='white')
dot = visual.Circle(win,radius=5,units="pix",fillColor=[1,1,1])

start = visual.TextStim(
	win,
	text="In this experiment you can only press either X or M. Press Any Key to Start",
	height=20,
	color='white'
)


start.draw()
win.flip()
event.waitKeys()

# 384, -384
dividerLow = visual.Line(
	win=win,
	start=(0,-584),
	end=(0,-400),
	lineColor=[1,0,0]
)
dividerHigh = visual.Line(
	win=win,
	start=(0,400),
	end=(0,584),
	lineColor=[1,0,0]
)

maxE=30
frameDur=30

def doTrial (mean):
	event.clearEvents()
	currentFrame=0
	x0=np.rint(np.random.normal(mean,100,size=maxE))
	x=np.repeat(x0,frameDur)
	resp=[]
	fix.draw()
	win.flip()
	core.wait(1)
	while (currentFrame<(maxE*frameDur) and len(resp)==0):		
		dividerLow.draw()
		dividerHigh.draw()
		dot.pos=[x[currentFrame],0]
		dot.draw()
		win.flip()
		currentFrame=currentFrame+1
		resp=event.getKeys(keyList=['x','m','escape'])
		if 'escape' in resp:
			fptr.close()
			win.close()
			return None, 'Abort', None
		elif resp:
			break
	return currentFrame,resp[0] if resp else None, x0



conditions = [-50,-50,-50,-50,-50,50,50,50,50,50]
random.shuffle(conditions)
for condition in conditions:
    [rt, resp, x] = doTrial(condition)
    if resp == 'Abort':
        print("Experiment Aborted")
        break
    print(sub, rt, resp, *x, sep=", ", file=fptr)
    fptr.flush()

fptr.close()
win.close()
core.quit()

