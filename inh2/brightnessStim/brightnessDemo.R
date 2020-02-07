circleDemo=function(color){
  par(mar=c(0,0,0,0), bg="grey50")
  plot(1, type="n", xlab="", ylab="", xlim=c(-4, 4), ylim=c(-4, 4), axes = FALSE)
  draw.circle(0, 0, 3, nv=1000, border = color, col = color)
}

target.color<-paste("grey", round(seq(25,75,length.out=10)),sep="")

# Demo
pdf(width=10,height=4,"demoCircle.pdf")
par(mfrow=c(2,5))
for(i in 0:9){
  circleDemo(color=target.color[i+1])
}
dev.off()