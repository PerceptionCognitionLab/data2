loc.data = "https://raw.githubusercontent.com/PerceptionCognitionLab/data2/master/out/efRsvp1.dat"
loc.session = "https://raw.githubusercontent.com/PerceptionCognitionLab/data2/master/out/session.info"

dat = read.table(url(loc.data), head=TRUE)
ses = read.table(url(loc.session), head=TRUE)

head(dat,10)
head(ses,10)

ses <- ses[,]

