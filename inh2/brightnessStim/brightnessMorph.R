library("plotrix")

myCircles=function(filename,colors){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0), bg='grey50')
  plot(1, type="n", xlab="", ylab="", xlim=c(-4, 4), ylim=c(-4, 4), axes = FALSE)
  draw.circle(0, 0, c(3, 1), nv=1000, border = colors, col = colors)
  dev.off()
}
myBlankCircles=function(filename,color){
  jpeg(filename,width=320,height=480)
  par(mar=c(0,0,0,0), bg='grey50')
  plot(1, type="n", xlab="", ylab="", xlim=c(-2, 2), ylim=c(-2, 2), axes = FALSE)
  draw.circle(0, 0, c(1), nv=1000, border = color, col = color)
  dev.off()
}

target.color<-paste("grey", round(seq(25,75,length.out=10)),sep="")

# Dark circles
for(i in 0:9){
  string=sprintf("%02d",i)
  filename=paste("Dark_circle_",string,".jpeg",sep="")
  colors=c("grey20", target.color[i+1])
  myCircles(filename,colors)
}

# Bright circles
for(i in 0:9){
  string=sprintf("%02d",i)
  filename=paste("Bright_circle_",string,".jpeg",sep="")
  colors=c("grey80", target.color[i+1])
  myCircles(filename,colors)
}

# Blank circles
for(i in 0:9){
  string=sprintf("%02d",i)
  filename=paste("Blank_circle_",string,".jpeg",sep="")
  colors=target.color[i+1]
  myBlankCircles(filename,colors)
}
