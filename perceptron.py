
#%%
import sys
import matplotlib.pyplot as plt

def updateWeights(x1,x2,y):
    global w0,w1,w2
    w0=w0+y
    w1=w1+y*x1
    w2=w2+y*x2

def isNum (temp):
    try:
        int(temp)
    except:
        return False
    return True

#MAIN

inpFile=sys.argv[1]
inpFile=open(inpFile,"r")
inp = inpFile.readlines()
inpFile.close()

outFile=sys.argv[2]
outFile=open(outFile,"w")

w0=0 # offset
w1=0 # x1 weight
w2=0 # x2 weight

errRate=1
turnNum=0

if len(inp):
    while (errRate>0.1):
        #init for plot
        trueSetX1=[]
        trueSetX2=[]
        falseSetX1=[]
        falseSetX2=[]
        #train      
        for x in range (0,len(inp)):
            line=inp[x]
            if len(line):
                line=line.split(",")
                if len(line)==3 and isNum(line[0]) and isNum(line[1]) and isNum(line[2]): 
                    x1=int(line[0])
                    x2=int(line[1])
                    y=int(line[2])
                    #get plot points
                    if y==1:
                        trueSetX1.append(x1)
                        trueSetX2.append(x2)
                    else:
                        falseSetX1.append(x1)
                        falseSetX2.append(x2)
                    #update weights if necessary
                    if (x1*w1+x2*w2+w0)*y<=0:
                        updateWeights(x1,x2,y)
                        outFile.write(str(w1)+","+str(w2)+","+str(w0)+"\n")

        #test
        errNum=0
        testNum=0
        if len(inp):
            for x in range (0,len(inp)):
                line=inp[x]
                if len(line):
                    line=line.split(",")
                    if len(line)==3 and isNum(line[0]) and isNum(line[1]) and isNum(line[2]): 
                        testNum+=1
                        x1=int(line[0])
                        x2=int(line[1])
                        y=int(line[2])
                        #check if err
                        if (x1*w1+x2*w2+w0)*y<=0:
                            errNum+=1
        #write results
        errRate=errNum/testNum
        turnNum+=1
        print("turn number: ",turnNum)
        print("w0: ",w0," w1: ",w1," w2: ",w2)
        print("err rate: ",errRate,"\n")

        #plot
        plt.plot(trueSetX1,trueSetX2,"go")
        plt.plot(falseSetX1,falseSetX2,"ro")
        plt.xlabel("x1")
        plt.ylabel("x2")
        title="turn:"+str(turnNum)+" w0:"+str(w0)+" w1:"+str(w1)+" w2:"+str(w2)+" err:"+str('{0:.2f}'.format(errRate))
        plt.title(title)
        totalBoundrySetX1=trueSetX1+falseSetX1
        totalBoundrySetX2=[]
        for x in range(0,len(totalBoundrySetX1)):
            totalBoundrySetX2.append((-w0-w1*totalBoundrySetX1[x])/w2)
        plt.plot(totalBoundrySetX1,totalBoundrySetX2)
        plt.show()

print("w0(offset)= ",w0," w1(weight of input1)= ",w1," w2(weight of input2)= ",w2,"\n")
outFile.close()
