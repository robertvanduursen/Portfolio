import pymel.core as pm
import pymel.core.datatypes as dt
import sys

obj = pm.ls(sl=1)[0]
print dir(obj)
print obj.inputs()
print obj.listAttr()


print pm.nodeOutliner(obj,q=1, showInputs=True)

import time
start = time.time()

allPos = []
for loc in pm.ls(sl=1): allPos += [tuple(pm.getAttr(loc.translate,t=fr)) for fr in pm.keyframe(loc.translateX,q=1,timeChange=1)] 
allSet = set(allPos)
myDict = dict(zip(allSet,[0] * len(allSet)))
#for x in allPos: myDict[x] += 1

'''
for pos,nr in myDict.items():
    loc = pm.spaceLocator()
    pm.xform(loc,t=dt.Vector(pos))
'''
	
posList = []
for pos,nr in myDict.items():
    posList.append(str((pos[0],pos[1],pos[2])))
command = "pm.polyCreateFacet(ch=0,tx=1,s=1,p=[{}])".format(','.join(posList))
eval(command)

end = time.time()
print (end-start)
