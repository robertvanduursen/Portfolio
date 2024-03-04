import pymel.core as pm
from maya import OpenMaya as om

mesh= pm.ls(sl=1)[0].getShape()
mesh_iterator = om.MItMeshPolygon(mesh.__apimdagpath__())

orig= [orig for orig in mesh.listHistory(type='mesh') if orig != mesh][0]
orig_iterator = om.MItMeshPolygon(orig.__apimdagpath__())

util = om.MScriptUtil()
util.createFromInt(0)
prev_ptr = util.asIntPtr()

val_X = om.MScriptUtil()
util.createFromDouble(0.00)
val_X_ptr = val_X.asDoublePtr()

meshDefDict = {}
total = 0

# Average point position of origMesh
for idx in range(mesh.numVertices()):
    mesh_iterator.setIndex(idx, prev_ptr)
    orig_iterator.setIndex(idx, prev_ptr)
    
    mesh_iterator.getArea(val_X_ptr)
    meshArea = val_X.getDouble(val_X_ptr)
    
    orig_iterator.getArea(val_X_ptr)
    origArea = val_X.getDouble(val_X_ptr)
    
    if abs(meshArea - origArea) > 0.5:
        #print idx
        total += 1
        meshDefDict[idx] = meshArea - origArea


print 'total ',total 

pm.select([mesh.f[x] for x in meshDefDict.keys()])