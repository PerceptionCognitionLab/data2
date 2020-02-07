getY <- function(r, theta) r*sin(theta)
getX <- function(r, theta) r*cos(theta)
rad  <- function(degrees) (degrees*pi)/180

myCircles <- function(filename, rTarget, r, nCircles=6){
  jpeg(filename,width=480,height=480)
  par(mar=c(0,0,0,0), bg='black')
  # center target
  theta   <- rad(seq(0, 360, length.out = 1e3))
  y       <- getY(r=rTarget, theta)
  x       <- getX(r=rTarget, theta)
  small_y <- getY(r, theta)
  small_x <- getX(r, theta)
  
  position <- rad(seq(0, 360, length.out = nCircles+1))
  position <- position[-length(position)]
  center_y <- getY(r=rTarget+r, position)
  center_x <- getX(r=rTarget+r, position)
  
  posLimit <- 7.2 # maximum value, if rTarget=2, r=2
  plot(x, y, type="l", xlab="", ylab="", xlim=c(-posLimit, posLimit), ylim=c(-posLimit, posLimit), axes = FALSE, lwd=3, col="white")
  for(i in seq_along(position)){
    new_circle_y <- center_y[i] + small_y
    new_circle_x <- center_x[i] + small_x
    points(new_circle_x, new_circle_y, type = 'l', lwd=3, col="white")
  }
  dev.off()
}

# Target stimuli
rTargets<-seq(1, 2, length.out = 8)

# Small Circles
r<-0.5
nCircles<-9
for(i in 0:7){
  string=sprintf("%02d",i)
  filename=paste("Small_circle_",string,".jpeg",sep="")
  rTarget=rTargets[i+1]
  myCircles(filename,rTarget,r,nCircles)
}

# Big Circles
r<-2.5
nCircles<-4
rTargets<-seq(1.2, 1.8, length.out = 8)

for(i in 0:7){
  string=sprintf("%02d",i)
  filename=paste("Large_circle_",string,".jpeg",sep="")
  rTarget=rTargets[i+1]
  myCircles(filename,rTarget,r,nCircles)
}
