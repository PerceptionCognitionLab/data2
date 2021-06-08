from psychopy import core, visual, sound, event
import random
import decimal
import sys
import numpy as np  
import os


##########################
# SET UP THE EXPERIMENT ##
##########################
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

dbConf = exp
print(SCRIPT_DIR)
print(dbConf)

scale=400

def readPoly (fname,scale):
    octoIN=np.loadtxt(fname,dtype=float)
    numPoly=int(max(octoIN[:,0]))
    numPoints=int(np.shape(octoIN)[0]/numPoly)
    octoIN=np.reshape(octoIN[:,1:3],(numPoly,numPoints,2))
    return(scale*(octoIN-.5))

dirname = os.path.dirname(__file__)
fname = os.path.join(dirname, '../dev/s1.octo')
octo=readPoly(fname,scale)

print(octo)