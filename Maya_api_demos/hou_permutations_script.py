node = hou.pwd()
geo = node.geometry()
import math

# generate binary subsets 

stamp = node.evalParm("stamp")
nrItems = node.evalParm('properties')
# Add code to modify contents of geo.

rangeList = []
rangeRange = 1
for prop in range(0,nrItems):
    minRange = node.evalParm('minmax'+str(prop)+'x')
    maxRange = node.evalParm('minmax'+str(prop)+'y')
    sizeRange = node.evalParm('size'+str(prop))+1
    totRange = maxRange - minRange
    rangeRange *= (sizeRange)
    rangeList.append((minRange,maxRange,rangeRange,sizeRange))

stepList = []
for prop in range(0,nrItems):
    partList = []
    for test in range(0,rangeList[prop][3]):
        step = hou.hmath.fit(test,0,rangeList[prop][3]-1,rangeList[prop][0],rangeList[prop][1])
        partList.append(round(step,2))
    stepList.append(tuple(partList))

#generate permutations
# Use drop down menu to select examples.
incr = 0
addBin = []
for each in range(0,rangeRange):
    tempBin = []
    for item in range(0,nrItems):
        if item==0:
            tempBin.append(int(each%rangeList[item][3]))
        else:
            #add incremental component here
            tempBin.append(int(math.floor(each/rangeList[item-1][2])%rangeList[item][3]))
    
    addBin.append(tempBin)
    #calcX = int(each%X)
    #calcY = int(math.floor(each/X)%Y)
    #calcZ = int(math.floor(each/(Y*X))%Z)
    #calcQ = int(math.floor(each/(Y*X*Z))%Q)
    #addBin.append(str([calcX,calcY,calcZ,calcQ]))

addBin.sort()

subSet = []
incr = 0
for item in addBin[stamp%len(addBin)]:
    subSet.append(stepList[incr][item])
    incr += 1

geo.addAttrib(hou.attribType.Global, "length",0)
geo.setGlobalAttribValue("length",len(addBin))

geo.addAttrib(hou.attribType.Global, "setLength",0)
geo.setGlobalAttribValue("setLength",len(subSet))

tempAttr = [0.0] * len(subSet)
geo.addAttrib(hou.attribType.Global, "subset",tempAttr)
geo.setGlobalAttribValue("subset",subSet)

geo.addAttrib(hou.attribType.Global, "_fd",'')
geo.setGlobalAttribValue("_fd",str(addBin))

geo.addAttrib(hou.attribType.Global, "_fds",'')
geo.setGlobalAttribValue("_fds",str(rangeList))

geo.addAttrib(hou.attribType.Global, "_fdz",'')
geo.setGlobalAttribValue("_fdz",str(stepList))
