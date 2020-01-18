import numpy 
import random

def rld(rl, numBack):
	cond = range(len(rl)*numBack)
        rlAll=rl*numBack
	output = numpy.repeat(cond, rlAll, axis=0)
	return(output.tolist())


# try out
numBack=2
numTarg=11
numCond=numBack*numTarg
rl=[2,3,4,5,6,7,6,5,4,3,2]

cond=rld(rl, numBack)

lenBlock=len(cond)
N=2*lenBlock

# Warm up trial
lenWarmUp=10
rlWarmUp=[1,1,1,1,1,1,1,1,1,1]
condWarmUp=rld(rlWarmUp, numBack)

for t in range(lenWarmUp):
	(blk,trl) = divmod(t,lenWarmUp)
	if trl==0 and blk>0:
		breakTxt.draw()
		window.flip()
		event.waitKeys()					 
	out=doTrial(condWarmUp[t],fp[t])
	(back,targ)=decode(condWarmUp[t])
    	rt = decimal.Decimal(out[1]).quantize(decimal.Decimal('1e-3'))
	addData = (sessionID, blk,trl,back,targ, int(fp[t]), out[0], rt)



