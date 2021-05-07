makeLine=function(x,y){
  l=1:2 #1=intercept, 2=slope 
  l[2]=(y[2]-y[1])/(x[2]-x[1])
  l[1]=y[1]-l[2]*x[1]
  return(l)}

intersection=function(l1,l2){
  x=(l2[1]-l1[1])/(l1[2]-l2[2])
  y=l1[2]*x+l1[1]
  return(c(x,y))
}
  
is.interior=function(xL,xU,ints){
  xL=sort(round(xL,6))
  xU=sort(round(xU,6))
  ints=round(ints,6)
  a=(xL[1]< ints[1] & ints[1] < xL[2])
  b=(xU[1]< ints[1] & ints[1] <xU[2])
  return(a&b)}

is.valid=function(a){
  s=NULL
  for (i in 1:8)
    for (j in 1:8){
      l1=makeLine(a$x[i:(i+1)],a$y[i:(i+1)])
      l2=makeLine(a$x[j:(j+1)],a$y[j:(j+1)])
      test=is.interior(a$x[i:(i+1)],a$x[j:(j+1)],intersection(l1,l2))
      s=c(s,as.integer(test))}
  return(sum(s,na.rm=T)==0)
}


oMake1=function(){
  x=runif(8,0,1)
  y=runif(8,0,1)
  oY=order(y)
  oYlow=oY[1:4]
  oYhi=oY[5:8]
  low=oYlow[order(x[oYlow])]
  hi=oYhi[order(x[oYhi],decreasing=T)]
  traj=c(low,hi,low[1])
  return(list(x=x[traj],y=y[traj]))}

oMake=function(format=T){
  flag=F
  while (!flag){
    a=oMake1()
    flag=is.valid(a)}
  if (format) out=cbind(a$x,a$y)
  else out=a
  return(out)}


vals=NULL
for (i in 1:2) vals=rbind(vals,oMake())
image=rep(1:2,c(9,9))
out=data.frame(image,vals)
write.table(file="s1.octo",out,row.names=F,quote=F,col.names=F)




