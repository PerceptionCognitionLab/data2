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



