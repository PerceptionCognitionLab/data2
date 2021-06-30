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

useDB=False
dbConf = exp
expName='costSave'
abortKey='q'

createTableStatement = (
    "CREATE TABLE `out__" + expName + "` ("
    "  `datID` INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `sessionID` INT(4) UNSIGNED NOT NULL,"
    "  `block` INT(2) UNSIGNED NOT NULL,"
    "  `trial` INT(2) UNSIGNED NOT NULL,"
    "  `stimGlobA` INT(3) UNSIGNED NOT NULL,"
    "  `stimGLobB` INT(1) UNSIGNED NOT NULL,"
    "  `weightA` DECIMAL(4.3) NOT NULL,"
    "  `correctResp` CHAR(1),"
    "  `resp` CHAR(1),"
    "  `rt`  DECIMAL(5,3),"
    "  PRIMARY KEY (`datID`)"
    ") ENGINE=InnoDB")

insertTableStatement = (
     "INSERT INTO `out__" + expName + "` ("
     "`sessionID`, `block`, `trial`, `stimGlobA`, `StimGlobB`, `weightA`, `correctResp`,`resp`,`rt`)"
     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

if useDB:
    sessionID=startExp(expName,createTableStatement,dbConf)
else:
	sessionID=1
    
########################################
# GLOBAL SETTINGS  #####################
########################################
window=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
    
########################################
# Functions  #####################
########################################

def initEsc(stim,mapping):
    K=len(stim)
    esc={}
    esc['stim']=stim
    esc['map']=mapping
    esc['o']=np.random.choice(K,K,replace=False)
    esc['current']=0
    esc['size']=0
    esc['set']=esc['o'][range(esc['size'])]
    return(esc)
    

def runEsc(esc):
    if (esc['current']==esc['size']):
        esc['size']=esc['size']+1
        esc['current']=0
        esc['set']=np.random.choice(esc['o'][0:esc['size']],
                                    esc['size'],
                                    replace=False)
        print("New Pair!")
        print("Stimulus " + 
              esc['stim'][esc['o'][esc['size']-1]] +
              ' Maps To ' +
              esc['map'][esc['o'][esc['size']-1]])
    val=esc['set'][esc['current']]    
    response=input("Trial. What maps to "+ esc['stim'][val] +"? ")
    if response == esc['map'][val]:
        esc['current']=esc['current']+1
        print("Correct")
    else:
        esc['current']=0
        esc['set']=np.random.choice(esc['o'][0:esc['size']],
                                    esc['size'],
                                    replace=False)
        print("Error! "+ 
              esc['stim'][val] + 
              " maps to " + 
              esc['map'][val])
    return(esc,response)
    
        
    
N=30 #total trials  
K=5 #upper number to learn per excalator
R=2 #number of escalators

stimLet=['A','B','C','D','E']
mapLet=['1','2','3','4','5']
stimPunc=['!','@','#','$','%']
mapPunc=['1','2','3','4','5']
a = [dict() for x in range(R)] #list of escalators
a[0]=initEsc(stim=stimLet,mapping=mapLet) #initialize each escalator
a[1]=initEsc(stim=stimPunc,mapping=mapPunc) #initialize each escalator

# lets just ron one escalator
for i in range(N):
    w=i%R
    [a[w],response]=runEsc(a[w])


