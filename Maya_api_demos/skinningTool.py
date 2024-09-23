# Import the required modules
from PySide import QtCore, QtGui, QtUiTools
import shiboken
import maya.OpenMayaUI as apiUI
import os

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import math


# TO ADD
#
# add / remove from skinCluster without weighting
# check connection of joint to skinclusters
# check the connection of skincluster to joints (i.e. influences)
#


###########################################################################
#METHODS
###########################################################################

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

def WHUT():
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


def inflObjs(select=False,skinClus=None):
    # something weird here with the last entry into the inlfuences list not being an actual path to any object..
    pathArray = om.MDagPathArray()
    skinClus.influenceObjects(pathArray)
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
        

###########################################################################
#CLASSES
###########################################################################

class SkinInfo():
    skinClus = None
    infls = []
    nrInfls = 0

    # Constructor
    def __init__(self):
        print 'skincluster found'
        self.skinClus = getSkincluster()[0]
        print self.skinClus
        objs = inflObjs(False,self.skinClus) # stored as a MDagPathArray
        self.infls = objs
        self.nrInfls = objs.length()
    
    def influences(self,api=False):
        newList = []
        for x in range(self.infls.length()):
            newList.append(self.infls[x].partialPathName())
        if api==True:
            return self.infls
        else:
            return newList

    def getNrInfls(self):
        return self.nrInfls
    
lol = SkinInfo()
print lol.getNrInfls()
lol.getNrInfls()
print 'the number of influences are ' + str(lol.getNrInfls())
print lol.influences().partialPathName()

# This class is used to open a Qt window in Maya using PySide
class ToolWindow():
    allInfl = []
    filterInfl = []
    skin = None

    # Constructor
    def __init__(self):
        self.uiFilePath = "D:/Library/Projects/Files/Script/Py/skinningTool/skinning.ui"
        self.MainWindow = None
        self.skin = SkinInfo()
 
    # Obtain the maya window wrapper to ensure correct window focusing
    def getMayaWindow():
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr is not None:
            return shiboken.wrapInstance(long(ptr), QtGui.QWidget)
 
    # Use PySide to load the ui file, converting it into a PySide QDialog object
    def loadUiWidget(self, uifilename, parent=getMayaWindow()):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        #ui = loader.load(uifile, parent)
        # if parent = none, standalone window launches
        ui = loader.load(uifile, None)

        uifile.close()
        return ui
 
    # Connect any signals in the ui file to required methods
    def connectSignals(self):
        # QT's objectname has to correspond with the name after 'MainWindow'
        self.MainWindow.pushButton.clicked.connect(self.mySignalMethod)
        self.MainWindow.pushButton_3.clicked.connect(self.mySignal)

        newItem = QtGui.QListWidgetItem("added items")
        self.MainWindow.listWidget.addItem(newItem)
        self.allInfl.append(newItem)
        newItem = QtGui.QListWidgetItem("dddd")
        self.MainWindow.listWidget.addItem(newItem)
        self.allInfl.append(newItem)
        newItem = QtGui.QListWidgetItem("lost items")
        self.MainWindow.listWidget.addItem(newItem)
        self.allInfl.append(newItem)
        

        self.MainWindow.scrollFilter.textChanged.connect(self.testSignal)
        

    # Signal method for when button is pushed
    def mySignalMethod(self):
        print 'mySignalMethod'
        mel.eval('ComponentEditor')

    def mySignal(self):
        print 'something else'

    def testSignal(self):
        print 'text updated'
        self.updateInflField()

    def updateInflField(self):
        # full list gets modified and 
        filterString = self.MainWindow.scrollFilter.text()
        print filterString
        for x in range(self.MainWindow.listWidget.count()):
            self.MainWindow.listWidget.takeItem(x)

        for x in self.allInfl:
            if filterString == '':
                self.MainWindow.listWidget.addItem(x)
            else:
                if filterString in x.text():
                    self.MainWindow.listWidget.addItem(x)
                else:
                    pass

        '''
        for x in range(self.MainWindow.listWidget.count()):
            print self.MainWindow.listWidget.item(x).text()
        '''
 
    # Show the dialog
    def show(self):
        self.close()
        app = QtGui.QApplication.instance()
        self.MainWindow = self.loadUiWidget(self.uiFilePath)
        self.connectSignals()  
        self.MainWindow.show()
        app.exec_()
 
    # Dispose the dialog
    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None

dialog = ToolWindow() 
dialog.show()



