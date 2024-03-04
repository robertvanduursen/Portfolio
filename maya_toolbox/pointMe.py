import pymel.core as pm
import pymel.core.datatypes as dt
import math

def pointMe():
    mods = pm.getModifiers()
    shift = False
    if (mods & 1) > 0: shift=True

    fromObj = pm.ls(sl=1)[0]
    toObj = pm.ls(sl=1)[1]
    if toObj.nodeType() == 'joint': toObj.jointOrient.set(0,0,0) 

    fromPos = dt.Vector(fromObj.getMatrix(worldSpace=1)[3][:-1])
    toPos = dt.Vector(toObj.getMatrix(worldSpace=1)[3][:-1])
    
    dir = (fromPos - toPos ).normal()
    side = (dt.Vector(0,1,0) ^ dir).normal()
    up = (dir ^ side).normal()
    
    newMatrix = toObj.getMatrix()
    newMatrix[0] = [dir.x,dir.y,dir.z,0.0]
    if shift:
		newMatrix[1] = [side.x,side.y,side.z,0.0]
		newMatrix[2] = [up.x,up.y,up.z,0.0]
    else:
		newMatrix[2] = [side.x,side.y,side.z,0.0]
		newMatrix[1] = [up.x,up.y,up.z,0.0]
		
    toObj.setMatrix(newMatrix)
   
pointMe()


