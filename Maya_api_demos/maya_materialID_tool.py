# script to try to make material ID assigning easier

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.OpenMayaUI as mui
import maya.OpenMayaAnim as oma
import math,sys


kPluginCtxName = 'idContext'
kPluginCmdName = 'idContextCmd'


class context(mpx.MPxContext):
    def __init__(self):
        mpx.MPxContext.__init__(self)
        print 'YES!'
    def doPress(self,event):
        sys.stderr.write('It works I hope!!!!!')
        print 'CLICK!'
        
class contextCommand(mpx.MPxContextCommand):
    def __init__(self):
        mpx.MPxContextCommand.__init__(self)
        print 'HE!'
    def makeObj(self):
        print 'TEST!'
        return mpx.asMPxPtr(context())

    @classmethod
    def creator(cls):
        return mpx.asMPxPtr(cls())


def initializePlugin(mobject):
    mplugin = mpx.MFnPlugin(mobject, "Passerby", "1.0", "Any")
    try:
        mplugin.registerContextCommand(kPluginCtxName, contextCommand.creator)
        print "succes"
    except:
        sys.stderr.write("Failed to register context command: %s\n" % kPluginCtxName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = mpx.MFnPlugin(mobject)
    try:
        mplugin.deregisterContextCommand(kPluginCtxName, kPluginCmdName)
    except:
        sys.stderr.write("Failed to deregister context command: %s\n" % kPluginCtxName)
        raise


#######################

def getMeshes():
    # get the skincluster of the mesh
    mSel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(mSel)

    #meshMObject = om.MObjectArray()
    iterSel = om.MItSelectionList(mSel)
    while not iterSel.isDone():
        #currentItem = iterSel.currentItem()
        #print currentItem
        meshDagPath  = om.MDagPath()
        meshMObject = om.MObject()
        #iterSel.getDependNode(0, meshMObject)
        iterSel.getDagPath(meshDagPath, meshMObject)
        print meshDagPath.fullPathName()
        meshDagPath.extendToShapeDirectlyBelow(0)
        print meshDagPath.fullPathName()
        
        if meshDagPath.node().hasFn(om.MFn.kMesh):
            skinFn = om.MFnMesh( meshDagPath.node())

            getCam = getCameraTransform()
            raySource = OpenMaya.MFloatPoint( getCam[0].x, getCam[0].y, getCam[0].z )
            rayDirection = getCam[1]
            #mFnMeshSrc.getVertexNormal( i, False, rayDirection)
            hitPoint = OpenMaya.MFloatPoint()

            # rest of the args
            hitFacePtr = OpenMaya.MScriptUtil().asIntPtr()
            idsSorted    = False
            testBothDirections = False
            faceIds      = None
            triIds       = None
            accelParams  = None
            hitRayParam  = None
            hitTriangle  = None
            hitBary1     = None
            hitBary2     = None
            maxParamPtr  = 99999999


            hit = skinFn.closestIntersection(raySource,
                    rayDirection,
                    faceIds,
                    triIds,
                    idsSorted,
                    OpenMaya.MSpace.kWorld,
                    maxParamPtr,
                    testBothDirections,
                    accelParams,
                    hitPoint,
                    hitRayParam,
                    hitFacePtr,
                    hitTriangle,
                    hitBary1,
                    hitBary2)


			if hit:
				print 'w00t'
            print 'yes'
        iterSel.next()


def getCameraTransform():
    # nice, but does not seem to work if the transform has a 

    mSel = om.MSelectionList()
    #om.MGlobal.getActiveSelectionList(mSel)
    mSel.add('|persp')
    meshMObject = om.MObject()

    meshDagPath = om.MDagPath()
    mSel.getDependNode(0, meshMObject)
    mSel.getDagPath(0, meshDagPath)
    print meshMObject.apiTypeStr()

    transF = om.MFnTransform(meshDagPath)
    test = transF.transformation()
    mtx = test.asMatrix()

    sel = cmds.ls(sl=1)
    pt0 = cmds.xform(sel[0],q=1,ws=1,t=1)
    camPos = om.MVector(pt0[0],pt0[1],pt0[2])

    camVec = om.MVector(mtx(2,0),mtx(2,1),mtx(2,2))
    newVec = camPos + (camVec * 2.0)

    #cmds.spaceLocator(p=(vec0.x,vec0.y,vec0.z))
    #cmds.spaceLocator(p=(vec1.x,vec1.y,vec1.z))
    #cmds.spaceLocator(p=(newVec.x,newVec.y,newVec.z))

    return camPos,camVec


 
# http://zoomy.net/2009/07/31/fastidious-python-shrub/
