import pymel.core as pm
import pymel.core.datatypes as dt
import math

bones = pm.ls(sl=1)
if len(bones) == 2:
    insertBones = 3
    start = dt.Vector(bones[0].getMatrix(worldSpace=1)[3][:-1])
    end = dt.Vector(bones[1].getMatrix(worldSpace=1)[3][:-1])
    dir = (end-start)
    port = dir/float(insertBones+1)
    
    for x in range(insertBones):
        pm.select(clear=1)
        jnt = pm.joint()
        pm.select(clear=1)
        bit = float(x)+1
        jnt.translate.set(start+(port*bit))