import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import sys
import maya.cmds as cmds

'''
NURBS patch skinning

using a nurbs patch's U value; skin a selection of vertices according to their U value on the patch. 
The maya's setting will have to be in centimeters and the patch has to be frozen

'''

currentUnits = cmds.currentUnit( query=True, linear=True )
if 'cm' not in currentUnits :
    cmds.currentUnit( linear='cm' )

def getCleanList(list):
    process = []
    modelname = list[1].split(".")[0]
    print modelname
    for vtx in list:
        if ":" in vtx:
            temp = vtx.split(":")
            end = int(temp[1][0:-1])
            start = int(temp[0].split("[")[1])
            
            for x in range(start,end+1):
                process.append((modelname + ".vtx[" + str(x) + "]"))

                
        else:
            process.append(vtx)
    return process


# get nurbs geometry reference - hard coded for now
nurbsRef = "nurbsPlane1"
nurbsShape = "nurbsPlaneShape1"



dag = om.MDagPath()
obj = om.MObject()
list = om.MSelectionList()
list.add(nurbsShape)
list.getDagPath(0, dag, obj)

# get the vertices
sel = cmds.ls(sl=1)
modelname = sel[0].split(".")[0]
shapeName = cmds.listRelatives(modelname,s=1)[0]
skinClus = cmds.listConnections(shapeName,t='skinCluster')[0]

vertList = getCleanList(sel)

pt = om.MPoint(0,0,0)
util = om.MScriptUtil()
tempU = util.asDoublePtr()
tempV = util.asDoublePtr()

curveFn = om.MFnNurbsSurface(dag)
jntNames = ['l_leg_foot_toe','l_leg_foot_mid_ik']

for vtx in vertList:
    # get the U value at the point closest to the nurbs patch
    vtxPos = cmds.xform(vtx,q=1,ws=1,t=1)
    pt = om.MPoint(vtxPos[0],vtxPos[1],vtxPos[2])
    closePt = curveFn.closestPoint(pt,False,tempU,tempV)
    util = om.MScriptUtil()
    U = util.asDoublePtr()
    V = util.asDoublePtr()

    curveFn.getParamAtPoint(closePt,U,V,om.MSpace.kObject)
    #curveFn.getParamAtPoint(closePt,U,V,om.MSpace.kWorld)
    
    gradient = util.getDouble(U)
    cmds.skinPercent( skinClus, vtx, transformValue=[(jntNames[0], gradient),(jntNames[1], 1.0-gradient)] )


##########################################

sel = cmds.ls(sl=1)[0]
dag = om.MDagPath()
obj = om.MObject()
list = om.MSelectionList()
list.add(sel)
list.getDagPath(0, dag, obj)

pt = om.MPoint(0,1,0)

util = om.MScriptUtil()
util.createFromList([0.0], 1)
U = util.asDoublePtr()
V = util.asDoublePtr()

curveFn = om.MFnNurbsSurface(dag)
closePt = curveFn.closestPoint(pt,False,U,V)
print closePt.x,closePt.y,closePt.z

for x in range(11):
    pt = om.MPoint()
    curveFn.getPointAtParam(1*(x*0.1),1*(x*0.1),pt)
    loc = cmds.spaceLocator(n='hey',p=(pt.x,pt.y,pt.z))[0]
    cmds.setAttr("%s.localScaleX" % loc,0.1*x)
    cmds.setAttr("%s.localScaleY" % loc,0.1*x)
    cmds.setAttr("%s.localScaleZ" % loc,0.1*x)