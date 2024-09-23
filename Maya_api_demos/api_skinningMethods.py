# select a mesh with a skin cluster and run the script

# functions to add:
#
# swap influences (in selection): exchange all the influence from one object to the other. I.e. set all vals of first to 0 and the second to X
# curve skinning
# mirror skin in axis / plane (experimental)
# query max influences and such
# minor tweaking tools
# tool to make influence transitions easier: i.e. have a vertices be affected by X influences
# edit members of the skincluster





import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import math

def getSkincluster():
    # get the skincluster of the mesh
    mSel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(mSel)
    meshMObject = om.MObject()
    #print meshMObject.apiTypeStr()

    meshDagPath  = om.MDagPath()
    mSel.getDependNode(0, meshMObject)
    mSel.getDagPath(0, meshDagPath)

    meshDagPath.extendToShapeDirectlyBelow(0)

    skinFn = None
    iterDg = om.MItDependencyGraph(meshDagPath.node(), om.MItDependencyGraph.kDownstream, om.MItDependencyGraph.kPlugLevel)
    while not iterDg.isDone():
        currentItem = iterDg.currentItem()
        if currentItem.hasFn(om.MFn.kSkinClusterFilter):
            skinFn = oma.MFnSkinCluster(currentItem)
            break
        iterDg.next()
    #print skinFn

    return skinFn,meshDagPath,meshMObject

def checkSkinVerts(skinClus):
    # check the skinCluster if every vertex of the MFnMesh is weighted
    weights = om.MDoubleArray()
    indexs = om.MIntArray()
    inflIndex = 0
    
    meshPath  = om.MDagPath()
    skinClus.getPathAtIndex(0,meshPath)
    #print meshPath.fullPathName()
    
    nonWeight = 0
    iterDg = om.MItMeshVertex(meshPath.node())

    while not iterDg.isDone():
        currentItem = iterDg.currentItem()
        #print currentItem.apiTypeStr()
        util = om.MScriptUtil()
        util.createFromInt(iterDg.index())
        intPtr = util.asUintPtr()
        skinClus.getWeights(meshPath,currentItem,weights,intPtr)
        if om.MScriptUtil().getUint(intPtr) == 0:
            nonWeight = 1
        iterDg.next()
    return nonWeight

sel = []
for x in cmds.ls(sl=1):
    skinner = getSkincluster()
    if checkSkinVerts(skinner[0]) == 1:
        sel.append(x)
if len(sel) > 1:
    cmds.select(sel)
else:
    print 'all skinned'


def inflIndex():
    path = om.MDagPath()
    getSkincluster()[0].indexForInfluenceObject(path)
    return path


def inflObjs(select=False):
    pathArray = om.MDagPathArray()
    getSkincluster()[0].influenceObjects(pathArray)
    if select:
        selectArray = []
        for c in select: selectArray.append(c)
        return selectArray
    else:
        return pathArray

def getWeights():

    weightDict = {}
    meshPath  = om.MDagPath()
    skinClus = getSkincluster()[0]
    skinClus.getPathAtIndex(0,meshPath)

    iterDg = om.MItMeshVertex(meshPath.node())

    while not iterDg.isDone():
        currentItem = iterDg.currentItem()
        #print currentItem.apiTypeStr()
        util = om.MScriptUtil()
        util.createFromInt(iterDg.index())
        intPtr = util.asUintPtr()

        weights = om.MDoubleArray()
        for c in range(2): weights.append(0.0)
        #print weights
        
        indexs = om.MIntArray()
        for c in range(2): indexs.append(c)
        #print indexs

        skinClus.getWeights(meshPath,currentItem,indexs,weights)
        weightDict[iterDg.index()] = weights
        print weights

        iterDg.next()


def setWeights():
    
    weightDict = {}
    meshPath  = om.MDagPath()
    skinClus = getSkincluster()[0]
    skinClus.getPathAtIndex(0,meshPath)

    iterDg = om.MItMeshVertex(meshPath.node())

    while not iterDg.isDone():
        currentItem = iterDg.currentItem()
        #print currentItem.apiTypeStr()
        util = om.MScriptUtil()
        util.createFromInt(iterDg.index())
        intPtr = util.asUintPtr()

        weights = om.MDoubleArray()
        for c in range(2): weights.append(0.0)
        #print weights
        
        indexs = om.MIntArray()
        for c in range(2): indexs.append(c)
        #print indexs

        skinClus.getWeights(meshPath,currentItem,indexs,weights)
        weightDict[iterDg.index()] = weights
        print weights

        iterDg.next()

def addInfl():
    # add directly to the bindpose and skincluster nodes
    # this may fuck up the interactive normalizing of weights
    
    # joint to skinCluster
        # jnt.message -> skinClus.paintTrans
        # jnt.objectColorRGB -> skinClus.influenceColor[x]
        # jnt.worldMatrix[0] -> skinClus.matrix[x]
    # joint to bindPose
        # jnt.message -> bindPose.members[x]
        # jnt.bindPose -> bindPose.worldMatrix[x]

    '''
    wits = getSkincluster()[0].findPlug('weights')
    wlPlug = getSkincluster()[0].findPlug('weightList')
    print wits.name()
    print wlPlug.name()
    print wlPlug.attribute().apiTypeStr()
    '''
    pass