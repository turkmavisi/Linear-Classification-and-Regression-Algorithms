#%%

import sys
import numpy as np
import math
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def isNumber (temp):
    try:
        float(temp)
    except:
        return False
    return True
#
def parse():
    global age,weight,height,inp,size
    for x in range (0,len(inp)):
        line=inp[x]
        line=line.split(",")
        if len(line)==3 and isNumber(line[0]) and isNumber(line[1]) and isNumber(line[2]):
            age.append(float(line[0]))
            weight.append(float(line[1]))
            height.append(float(line[2]))
    size=len(height)
#
def plotData(turnNumber,err,iterationNumber):
    global normalizedAge,normalizedWeight,calculatedHeight,height,alist
    z = lambda x,y: calculate(x,y)
    tmp = np.linspace(-2,2,51)
    x,y = np.meshgrid(tmp,tmp)
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')
    normalizedAge =  np.array(normalizedAge)
    normalizedWeight = np.array(normalizedWeight)
    ax.scatter(normalizedAge,normalizedWeight,height,c="r")
    ax.plot_surface(x, y, z(x,y))
    ax.set_xlabel('Age(year)')
    ax.set_ylabel('Weight(kg)')
    ax.set_zlabel('Height(m)')
    info="turn number "+str(turnNumber)+": "+str(iterationNumber)+" iteartion done with alpha= "+str(alist[turnNumber])+"\nerror= "+str(err)
    ax.text2D(0.05, 0.95, info, transform=ax.transAxes)
    plt.show()
#
def mean (data):
    global size
    sum=0
    for x in range (0,size):
        sum=sum+data[x]
    return sum/size
#
def standardDeviation(data,dataMean):
    global size
    temp=[]
    for x in range(0,size):
        a=data[x]-dataMean
        temp.append(a*a)
    devSqr=mean(temp)
    return math.sqrt(devSqr)
#
def normalize():
    global age,weight,normalizedAge,normalizedWeight,size
    ageMean=mean(age)
    weightMean=mean(weight)
    ageDeviation=standardDeviation(age,ageMean)
    weightDeviation=standardDeviation(weight,weightMean)
    for x in range (0,size):
        normalizedAge.append((age[x]-ageMean)/ageDeviation)
        normalizedWeight.append((weight[x]-weightMean)/weightDeviation)
#
def calculate(age,weight):
    global b0,b1,b2
    return b0+b1*age+b2*weight
#
def calculateHeights():
    global normalizedAge,normalizedWeight,calculatedHeight,size
    for x in range (0,size):
        calculatedHeight.append(calculate(normalizedAge[x],normalizedWeight[x]))
#
def error():
    global calculatedHeight,height,b0,b1,b2,size
    ssr=0
    for x in range(0,size):
        try:
            ssr=ssr+math.pow(height[x]-calculatedHeight[x],2) 
        except OverflowError:
            print("ovrflw")
            return float('inf')
    return ssr/(2*size)
#
def update():
    global normalizedAge,normalizedWeight,height,b0,b1,b2,a,size
    tempb0=0
    tempb1=0
    tempb2=0
    for x in range (0,size):
        temp=calculate(normalizedAge[x],normalizedWeight[x])-height[x]
        tempb0=tempb0+temp
        tempb1=tempb1+temp*normalizedAge[x]
        tempb2=tempb2+temp*normalizedWeight[x]
    b0=b0-a*tempb0/size
    b1=b1-a*tempb1/size
    b2=b2-a*tempb2/size
#
def reset():
    global b0,b1,b2,calculatedHeight
    del calculatedHeight[:]
    b0=0
    b1=0
    b2=0
#Main

inpFile=sys.argv[1]
inpFile=open(inpFile,"r")
inp = inpFile.readlines()
inpFile.close()

outFile=sys.argv[2]
outFile=open(outFile,"w")

age=[]
normalizedAge=[]
weight=[]
normalizedWeight=[]
height=[]
calculatedHeight=[]
size=0

b0=0
b1=0
b2=0
alist=[0.001,0.005,0.01,0.05,0.1,0.5,1,5,10]
a=0
errtemp=[float("inf"),0]

parse()
normalize()
for x in range (0,len(alist)):
    a=alist[x]
    for y in range (0,100):
        update()
    calculateHeights()
    err=error()
    print("error in simulation number ",x," with 100 iterations= ",err)
    plotData(x,err,100)
    if errtemp[0]>err:
        errtemp[0]=err
        errtemp[1]=x
    outFile.write(str(a)+","+str(100)+","+str(b0)+","+str(b1)+","+str(b2)+"\n")
    reset()
a=alist[errtemp[1]]
alist.append(a)
for x in range (0,1000):
    update()
calculateHeights()
err=error()
print("error in simulation number ",errtemp[1]," with 1000 iterations= ",err)
plotData(9,err,1000)
outFile.write(str(a)+","+str(1000)+","+str(b0)+","+str(b1)+","+str(b2))
outFile.close()

input()