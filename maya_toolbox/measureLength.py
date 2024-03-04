import pymel.core as pm
import pymel.core.datatypes as dt
import math
bones = pm.ls(sl=1)
leng = 0.0
for idx in range(len(bones)-1):
    vec1 = dt.Vector(pm.xform(bones[idx],q=1,ws=1,t=1))
    vec2 = dt.Vector(pm.xform(bones[idx+1],q=1,ws=1,t=1))
    boneLeng = (vec1-vec2).length()
    #print boneLeng
    leng += boneLeng
print leng