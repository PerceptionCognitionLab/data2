import numpy as np
from collections import namedtuple

top=10  #max stim to learn
N=10 #total trials


stim=np.random.choice(np.array(range(top)),size=top,replace=False)
current=0
set=stim[range(current)]
