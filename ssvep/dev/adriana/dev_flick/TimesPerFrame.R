setwd("/home/exp/local-exp/pythonSetup/skel/dev_flick/")

datos <- read.csv("Erik10_2021-01-31.csv")
length(datos$Duration)

summary(datos$Duration[1:240])
summary(datos$Duration[241:480])

plot(c(1:240))

hist(datos$Duration)