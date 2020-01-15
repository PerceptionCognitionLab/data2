import numpy 

def rld(runlengths):
	cond = range(len(runlengths))
	output = numpy.repeat(cond, runlengths, axis=0)
	return(output)

def totalRunlength(runlengthPerCondition, ncond):
	output = numpy.repeat(runlengthPerCondition, ncond, axis=0)
	return(output)

