import maya.cmds as cmds
import math
import maya.OpenMaya as om

currentUnits = cmds.currentUnit( query=True, linear=True )
if 'cm' not in currentUnits :
    cmds.currentUnit( linear='cm' )

    
# acces the U value of the curve through OpenMaya
mSel = om.MSelectionList()
om.MGlobal.getActiveSelectionList(mSel)
dag  = om.MDagPath()
mSel.getDagPath(0, dag)

nurbsFn = om.MFnNurbsSurface(dag)

loc = om.MPoint(0.0,0.0,0.0)

util = OpenMaya.MScriptUtil()
util.createFromList([1.0], 1)
u_point = util.asDoublePtr()
v_point = util.asDoublePtr()



for x in range(0,10):
    loc = om.MPoint(0.0,0.0,0.0)

    util = OpenMaya.MScriptUtil()
    util.createFromList([1.0], 1)
    u_point = util.asDoublePtr()
    v_point = util.asDoublePtr()
    nurbsFn.getPointAtParam((1.0/9)*x,(1.0/9)*x, loc,OpenMaya.MSpace.kWorld)
    print x
    cmds.spaceLocator(p=[loc.x,loc.y,loc.z])

