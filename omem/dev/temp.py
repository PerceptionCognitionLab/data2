import numpy as np  

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


