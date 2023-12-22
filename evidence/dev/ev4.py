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
	text="Press Any Key to Start",
	height=20,
	color='white'
)



start.draw()
win.flip()
event.waitKeys()

divider = visual.Line(
	win=win,
	start=(0,-384),
	end=(0,384),
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
	while (currentFrame<(maxE*frameDur) and len(resp)==0):		
		divider.draw()
		dot.pos=[x[currentFrame],0]
		dot.draw()
		win.flip()
		currentFrame=currentFrame+1
		resp=event.getKeys()
		if 'escape' in resp:
			return None, 'Abort', None
	return(currentFrame,resp[0],x0)



initial_condition = -50
num_trials = 4
for i in range(num_trials):
	[rt, resp, x] = doTrial(initial_condition)
	if resp == 'Abort':
		print("Experiment Aborted")
		break
	print(sub, rt, resp, *x, sep=", ", file=fptr)
	fptr.flush()
	initial_condition *= -1


fptr.close()
win.close()
core.quit()

