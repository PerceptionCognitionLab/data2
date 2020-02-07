getY <- function(r, theta) r*sin(theta)
getX <- function(r, theta) r*cos(theta)
rad  <- function(degrees) (degrees*pi)/180

myBlankCircles=function(r){
  # center target
  theta   <- rad(seq(0, 360, length.out = 1e3))
  y       <- getY(r, theta)
  x       <- getX(r, theta)
  
  posLimit <- 4.4 # maximum value, if rTarget=2
  plot(x, y, type="l", xlab="", ylab="", xlim=c(-posLimit, posLimit), ylim=c(-posLimit, posLimit), axes = FALSE, lwd=3, col="white")
  
  #  dev.off()
}

rTargets<-seq(1, 2, length.out = 8)

pdf(width=10,height=5,"demoCircle.pdf")
par(mar=c(0,0,0,0), bg='black', par(mfrow=c(2,4)))
for(i in 0:7){
  myBlankCircles(rTargets[i+1])
}
dev.off()



