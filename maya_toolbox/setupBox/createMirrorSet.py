# this test executed on 80,000 vertices sphere and 6 faces box
from time import time
from maya import OpenMaya as om
import pymel.core as pm
from pymel.core import *
import math

node = pm.ls(sl=1)[0]
d = api.toMDagPath(node.nodeName())
d.extendToShape()
dmfn = om.MFnMesh(d)
s = om.MSpace.kWorld
pts = om.MPointArray()
dmfn.getPoints(pts, s)

setPts = []
for i in xrange(pts.length()):
    vec = om.MVector(pts[i])*0.01
    if abs(vec.x) < 0.001: 
        setPts.append(node.vtx[i])

mids = set(node.getShape().verts) - set(setPts)

pm.select(clear=1)
vertSet = pm.sets(n='mirrorVerts')
pm.sets(vertSet ,e=1,add=mids)
