loopCount=0
for i in range(len(dataSet)):
   for x in range(len(dataSet)-i-1):
      if dataSet[x]>dataSet[x+1]:
        tmp=dataSet[x]
        dataSet[x]=dataSet[x+1]
        dataSet[x+1]=tmp
      loopCount+=1
   print dataSet
print "最后结果：%s"%dataSet
print "loop times  %s"%loopCount
