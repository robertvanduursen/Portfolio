import pymel.core as pm
import pymel.core.datatypes as dt
import sys
import maya.OpenMaya as OpenMaya

import time
start = time.time()

allPos = []
for loc in pm.ls(sl=1): allPos += [tuple(pm.getAttr(loc.translate,t=fr)) for fr in pm.keyframe(loc.translateX,q=1,timeChange=1)] 
allSet = set(allPos) # all the unique points
myDict = dict(zip(allSet,[0] * len(allSet)))
for x in allPos: myDict[x] += 1

newList = []
maxNr = 0.0
for pos,nr in myDict.items():
    newList.append((pos,nr))
    if nr > maxNr: maxNr = nr


posList = []
for item in newList:
    pos = item[0]
    posList.append(str((pos[0],pos[1],pos[2])))
command = "pm.polyCreateFacet(ch=0,tx=1,s=1,p=[{}])".format(','.join(posList))
eval(command)

end = time.time()
print (end-start)


myMesh = pm.ls(sl=1)[0]
myMesh.vertexColorSource.set(1)
myMesh.displayVertices.set(1)
#print myMesh.currentColorSet.get()
pm.polyColorPerVertex( g =1.0, a= 1, cdo=1 )
pm.toggle(myMesh,state=False, g=True )

# bracketing

def bracket(curVal,maxVal,nrBrackets,normalize):
    ''' return the value in the correctsponding '''
    portions = maxVal / nrBrackets
    curBrack = 1
    notSelf = True
    incr = 0
    while notSelf and incr < 10:
        rem = (portions*curBrack) % curVal
        if rem == portions*curBrack:
            curBrack+=1
        else:
            notSelf = False
        incr +=1
    
	return (curBrack-1,float(portions*(curBrack-1)) / curVal)


print bracket(70,159,3,0)


# colour the points
sel = pm.selected()[0]
shape = sel.getShape()

mobj = shape.__apimobject__()
meshFn = OpenMaya.MFnMesh(mobj)

vertexColorList = OpenMaya.MColorArray()
normalsList = OpenMaya.MFloatVectorArray()

meshFn.getVertexColors(vertexColorList)
meshFn.getNormals(normalsList)

lenVertexList = vertexColorList.length()

fnComponent = OpenMaya.MFnSingleIndexedComponent()
fullComponent = fnComponent.create( OpenMaya.MFn.kMeshVertComponent )

fnComponent.setCompleteData( lenVertexList );

vertexIndexList = OpenMaya.MIntArray()
fnComponent.getElements(vertexIndexList)
print 'hey',len(newList)
maxNr = float(maxNr)
for k in range(lenVertexList):
    
	brack,val = bracket(newList[k][1],maxNr,3,0)
	[vertexColorList[k].r,vertexColorList[k].g,vertexColorList[k].b][brack] = val
	
	#vertexColorList[k].g = float(newList[k][1]) / maxNr
	#vertexColorList[k].b = newList[k][1]

print 'yey'

meshFn.setVertexColors(vertexColorList,vertexIndexList, None)

