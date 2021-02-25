data <- read.table("timing.dat")
dim(data)
head(data,5)
d<-data$V3-data$V2
plot(d, ylim=c(0.02,0.03))
summary(d)






