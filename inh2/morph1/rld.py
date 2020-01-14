import numpy


def rld(runLengths, cond)
	x = np.array(cond)
	output = np.repeat(x, runLengths, axis=0)
	return(output) 


def jeffs(runlengths):
	x=range(len(runlengths))
	output = np.repeat(x, runlengths, axis=0)
	return(output)
