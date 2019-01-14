### Program for creating the flanker effect stimuli



# colors!
invertColors=TRUE

### general variables
background=c(1:4,6:9)
wbackground=c(1,3,4,6,7,9)
sep=.1
dist=1+sep
x=c(0,0,0,1,1,1,2,2,2)*dist
y=c(0,1,2,0,1,2,0,1,2)*dist

### FUNCTIONS USED
myLet=function(a,pos){
  b=(-1/9)*a+(1/18)
  x1=x[pos]+c(0+b,1-b,(a/2)+(b))
  x2=x[pos]+c(a+b,1-a-b,1-(a/2)-b)
  y1=y[pos]+c(0,0,.5)
  y2=y[pos]+c(1,1,.5)
  segments(x1,y1,x2,y2,lwd=7)
}

myBox=function(pos){
  z0=0
  z1=1		
  x1=x[pos]+c(z0,z0,z1,z1,z0,z1)
  x2=x[pos]+c(z0,z1,z1,z0,z1,z0)
  y1=y[pos]+c(0,1,1,0,0,0)
  y2=y[pos]+c(1,1,0,0,1,1)
  segments(x1,y1,x2,y2,lwd=7)
}

myC=function(pos){
  z0=.2
  z1=.78
  x1=x[pos]+c(z1,z0,z0)
  x2=x[pos]+c(z0,z0,z1)
  y1=y[pos]+c(0,0,1)
  y2=y[pos]+c(0,1,1)
  segments(x1,y1,x2,y2,lwd=7)
}

myT=function(pos){
  z0=0
  z1=1
  x1=x[pos]+c(.5,z0)
  x2=x[pos]+c(.5,z1)
  y1=y[pos]+c(z0,z1)
  y2=y[pos]+c(z1,z1)
  segments(x1,y1,x2,y2,lwd=7)
}

myE=function(pos){
  z0=.1
  z1=.9
  x1=x[pos]+c(z1,z0,z0,z0)
  x2=x[pos]+c(z0,z0,z1,z0+.67*(z1-z0))
  y1=y[pos]+c(0,0,1,.5)
  y2=y[pos]+c(0,1,1,.5)
  segments(x1,y1,x2,y2,lwd=7)
}

cat=function(filename,center){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0))
  plot(c(0,3*dist),c(0,3*dist),axes=F,typ='n')
  for (i in wbackground) 
    myBox(i)
  myC(2)
  myLet(center/2,5)
  myT(8)
  dev.off()
}


the=function(filename,center){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0))
  plot(c(0,3*dist),c(0,3*dist),axes=F,typ='n')
  for (i in wbackground) 
    myBox(i)
  myT(2)
  myLet(center/2,5)
  myE(8)
  dev.off()
}

myArray=function(filename,center,surround){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0))
  if (invertColors) par(fg='white',bg='black')
  plot(c(0,3*dist),c(0,3*dist),axes=F,typ='n')
  for (i in background) 
    myLet(surround/2,i)
  myLet(center/2,5)
  dev.off()
}

myArray0=function(filename,center){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0))
  if (invertColors) par(fg='white',bg='black')  
  plot(c(0,3*dist),c(0,3*dist),axes=F,typ='n')
  myLet(center/2,5)
  dev.off()
}


myArrayBox=function(filename,center,surround){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0))
  if (invertColors) par(fg='white',bg='black')
  plot(c(0,3*dist),c(0,3*dist),axes=F,typ='n')
  for (i in background) 
    myBox(i)
  myLet(center/2,5)
  dev.off()
}



### LOOPS TO MAKE THE STIMULI
### Frame is all A's
for ( i in 0:20){
  filename=paste("FA_T",i,".jpeg",sep="")
  cen=i/20
  myArray(filename,center=cen,surround=1)
}

### Frame is all H's
for ( i in 0:20){
  filename=paste("FH_T",i,".jpeg",sep="")
  cen=i/20
  myArray(filename,center=cen,surround=0)
}

### Frame is w/o background
for ( i in 0:20){
  filename=paste("T",i,".jpeg",sep="")
  cen=i/20
  myArray0(filename,center=cen)
}

### Frame is box background
for ( i in 0:20){
  filename=paste("X_T",i,".jpeg",sep="")
  cen=i/20
  myArrayBox(filename,center=cen)
}

### Frame is "CAT"
for ( i in 0:20){
  filename=paste("CAT_T",i,".jpeg",sep="")
  cen=i/20
  cat(filename,center=cen)
}

### Frame is "THE"
for ( i in 0:20){
  filename=paste("THE_T",i,".jpeg",sep="")
  cen=i/20
  the(filename,center=cen)
}
