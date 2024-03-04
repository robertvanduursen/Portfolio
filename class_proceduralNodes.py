# base node class

import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.cmds as cmds
import sys

class procNetwork():
    hasMatrix = False
    selected_0 = ''
    selected_1 = ''

    def __init__(self,hasMatrix=False,selected_0='',selected_1=''):
        self.checkPlugin()
        print 'normalize node created'
        if hasMatrix == True:
            hasMatrix = True
            print 'with matrix'

    def append():
        pass
        #append a normalize to a newtork

    def checkConnection(self,sel):
        # returns a bool if the joint is already connected
        check = cmds.listConnections(sel, t='decomposeMatrix')
        if check != None and len(check) > 0:
            return check[0]
        else:
            return False


    def checkPlugin(self):
        # check if the matrix nodes plug-in is loaded
        check = cmds.pluginInfo('matrixNodes.mll', query=True, l=True)
        if check == False:
            cmds.loadPlugin('matrixNodes.mll')
            print 'plugin activated'
        elif check==True:
            print 'plugin already loaded'
        else:
            print 'nothing loaded'

    def createMatrix(self, name='getWorldPos'):
        # create a decomposeMatrix node
        matrix = cmds.shadingNode('decomposeMatrix',asUtility = True, n=name)
        return matrix

    def getMatrix(self,node):
        if self.checkConnection(node) == False:
            matrix1 = self.createMatrix('testName')
            cmds.connectAttr(("%s.worldMatrix[0]" % str(node)), ("%s.inputMatrix" %str(matrix1)), force=True)
        else:
            matrix1 = self.checkConnection(node)

        return matrix1


    def getOutputAttr(self,obj):
        outputAttrs = cmds.listAttr(obj, c=True,o=True)
        if 'outputX' in outputAttrs:
            outAttr = 'output'
        elif 'output3D' in outputAttrs:
            outAttr = 'output3D'
        elif 'outputTranslate' in outputAttrs:
            outAttr = 'outputTranslate'
        elif 'translate' in outputAttrs:
            outAttr = 'translate'

        return outAttr

    def length(self,vector=None):
        # set up a network of nodes to create a 'length' function
        # i.e. 
        if vector != None:
            vec = vector
        else:
            vec = cmds.ls(sl=1)[0]

        # connect the selected node based on the flags
        outAttr = self.getOutputAttr(vec)

        powerNode = cmds.shadingNode('multiplyDivide',asUtility = True, n='power')
        cmds.setAttr( "%s.operation" % str(powerNode), 3)
        cmds.setAttr( "%s.input2X" % str(powerNode), 2)
        cmds.setAttr( "%s.input2Y" % str(powerNode), 2)
        cmds.setAttr( "%s.input2Z" % str(powerNode), 2)

        sumValues = cmds.shadingNode('plusMinusAverage',asUtility = True, n='sumVals')

        squareNode = cmds.shadingNode('multiplyDivide',asUtility = True, n='length')
        cmds.setAttr( "%s.operation" % str(squareNode), 3)
        cmds.setAttr( "%s.input2X" % str(squareNode), 0.5)
        cmds.setAttr( "%s.input2Y" % str(squareNode), 0.5)
        cmds.setAttr( "%s.input2Z" % str(squareNode), 0.5)

        cmds.connectAttr(("%s.outputX" % str(powerNode)), ("%s.input1D[0]" %str(sumValues)), force=True)
        cmds.connectAttr(("%s.outputY" % str(powerNode)), ("%s.input1D[1]" %str(sumValues)), force=True)
        cmds.connectAttr(("%s.outputZ" % str(powerNode)), ("%s.input1D[2]" %str(sumValues)), force=True)

        cmds.connectAttr(("%s.output1D" % str(sumValues)), ("%s.input1X" %str(squareNode)), force=True)

        cmds.connectAttr(("%s.%s" % (str(vec),str(outAttr))), ("%s.input1" %str(powerNode)), force=True)

        endNode = squareNode
        return endNode,vec

    def normalize(self,vec,lengthNode,lengthAttr='outputX'):
        # this function only appends the normalization on a vector, not as a seperate network
        # i.e. a vector divides by its own length/magnitude
        # i.e. vec / vec.mag()
        outPut = ''
        outPut = self.getOutputAttr(vec)

        divNode = cmds.shadingNode('multiplyDivide',asUtility = True, n='normalize')
        cmds.setAttr( "%s.operation" % str(divNode), 2)

        cmds.connectAttr(("%s.%s" % (str(vec),str(outPut))), ("%s.input1" %str(divNode)), force=True)

        cmds.connectAttr(("%s.%s" % (str(lengthNode),str(lengthAttr))), ("%s.input2X" %str(divNode)), force=True)
        cmds.connectAttr(("%s.%s" % (str(lengthNode),str(lengthAttr))), ("%s.input2Y" %str(divNode)), force=True)
        cmds.connectAttr(("%s.%s" % (str(lengthNode),str(lengthAttr))), ("%s.input2Z" %str(divNode)), force=True)

        return divNode


    def dotProduct(self,vec0,vec1):
        # set up a dot product network - this does need two vectors - a.dot(b)=a1*b1+a2*b2.
        matrix1 = self.getMatrix(vec0)
        matrix2 = self.getMatrix(vec1)
        multiCompNode = cmds.shadingNode('multiplyDivide',asUtility = True, n='multiplyComponents')
        sumResults = cmds.shadingNode('plusMinusAverage',asUtility = True, n='sumResults')

        cmds.connectAttr(("%s.worldMatrix[0]" % str(joint1)), ("%s.inputMatrix" %str(matrix1)), force=True)
        cmds.connectAttr(("%s.worldMatrix[0]" % str(joint2)), ("%s.inputMatrix" %str(matrix2)), force=True)


        cmds.connectAttr(("%s.outputTranslate" % str(matrix1)), ("%s.input1" %str(multiCompNode)), force=True)
        cmds.connectAttr(("%s.outputTranslate" % str(matrix2)), ("%s.input2" %str(multiCompNode)), force=True)

        cmds.connectAttr(("%s.outputX" % str(multiCompNode)), ("%s.input1D[0]" %str(sumResults)), force=True)
        cmds.connectAttr(("%s.outputY" % str(multiCompNode)), ("%s.input1D[1]" %str(sumResults)), force=True)
        cmds.connectAttr(("%s.outputZ" % str(multiCompNode)), ("%s.input1D[2]" %str(sumResults)), force=True)

    def crossProduct(self,vec0,vec1):
        # setup to calculate a cross vector of two vectors

        '''
            c_x = (a_y*b_z) - (a_z*b_y)
            c_y = (a_z*b_x) - (a_x*b_z)
            c_z = (a_x*b_y) - (a_y*b_x)
        '''

        outAttr_vec0 = self.getOutputAttr(vec0)
        outAttr_vec1 = self.getOutputAttr(vec1)

        multi_0 = cmds.shadingNode('multiplyDivide',asUtility = True, n='cross_multi')
        multi_1 = cmds.shadingNode('multiplyDivide',asUtility = True, n='cross_multi')
        subs = cmds.shadingNode('plusMinusAverage',asUtility = True, n='cross_sub')
        cmds.setAttr( "%s.operation" % str(subs), 2)

        # C_X
        cmds.connectAttr((("%s."+outAttr_vec0+"Y") % str(vec0)), ("%s.input1X" %str(multi_0)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"Z") % str(vec1)), ("%s.input2X" %str(multi_0)), force=True)

        cmds.connectAttr((("%s."+outAttr_vec0+"Z") % str(vec0)), ("%s.input1Y" %str(multi_0)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"Y") % str(vec1)), ("%s.input2Y" %str(multi_0)), force=True)

        # C_Y
        cmds.connectAttr((("%s."+outAttr_vec0+"Z") % str(vec0)), ("%s.input1Z" %str(multi_0)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"X") % str(vec1)), ("%s.input2Z" %str(multi_0)), force=True)

        cmds.connectAttr((("%s."+outAttr_vec0+"X") % str(vec0)), ("%s.input1X" %str(multi_1)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"Z") % str(vec1)), ("%s.input2X" %str(multi_1)), force=True)

        # C_Z
        cmds.connectAttr((("%s."+outAttr_vec0+"X") % str(vec0)), ("%s.input1Y" %str(multi_1)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"Y") % str(vec1)), ("%s.input2Y" %str(multi_1)), force=True)

        cmds.connectAttr((("%s."+outAttr_vec0+"Y") % str(vec0)), ("%s.input1Z" %str(multi_1)), force=True)
        cmds.connectAttr((("%s."+outAttr_vec1+"X") % str(vec1)), ("%s.input2Z" %str(multi_1)), force=True)

        # sub input3D[0].input3Dx
        cmds.connectAttr(("%s.outputX" % str(multi_0)), ("%s.input3D[0].input3Dx" %str(subs)), force=True)
        cmds.connectAttr(("%s.outputY" % str(multi_0)), ("%s.input3D[1].input3Dx" %str(subs)), force=True)

        cmds.connectAttr(("%s.outputZ" % str(multi_0)), ("%s.input3D[0].input3Dy" %str(subs)), force=True)
        cmds.connectAttr(("%s.outputX" % str(multi_1)), ("%s.input3D[1].input3Dy" %str(subs)), force=True)

        cmds.connectAttr(("%s.outputY" % str(multi_1)), ("%s.input3D[0].input3Dz" %str(subs)), force=True)
        cmds.connectAttr(("%s.outputZ" % str(multi_1)), ("%s.input3D[1].input3Dz" %str(subs)), force=True)

        return subs


    def lengthVector(self,obj0=None,obj1=None):
        # get the length vector between two objects
        if obj0 != None:
            matrix1 = self.getMatrix(obj0)
            matrix2 = self.getMatrix(obj1)
        else:
            sel = cmds.ls(sl=1)
            matrix1 = self.getMatrix(sel[0])
            matrix2 = self.getMatrix(sel[1])

        subtractVectors = cmds.shadingNode('plusMinusAverage',asUtility = True, n='subVectors')
        cmds.setAttr( "%s.operation" % str(subtractVectors), 2)

        cmds.connectAttr(("%s.outputTranslate" % str(matrix1)), ("%s.input3D[0]" %str(subtractVectors)), force=True)
        cmds.connectAttr(("%s.outputTranslate" % str(matrix2)), ("%s.input3D[1]" %str(subtractVectors)), force=True)

        return subtractVectors,matrix1,matrix2


    def setRange(self,node,val,oldMin,oldMax,newMin,newMax,v=1):
        # node network for the creation of a setrange function

        # options should inlcude support for 3 inputs (i.e. a vector) and 1 input
        # this affects the setting / connecting of attributes!!
        refVal = node + '.' +  val

        # creating nodes and setting parameters
        defaultSub = cmds.shadingNode('plusMinusAverage',asUtility = True, n='defaultSub')
        cmds.setAttr( "%s.operation" % str(defaultSub), 2)
        if v == 1:
            cmds.connectAttr(refVal, ("%s.input3D[0].input3Dx" %str(defaultSub)), force=True)
        else:
            cmds.connectAttr(refVal, ("%s.input3D[0]" %str(defaultSub)), force=True)
        
        cmds.setAttr( "%s.input3D[1].input3Dx" % str(defaultSub), oldMin)
        cmds.setAttr( "%s.input3D[1].input3Dy" % str(defaultSub), oldMin)
        cmds.setAttr( "%s.input3D[1].input3Dz" % str(defaultSub), oldMin)

        diffNew = cmds.shadingNode('plusMinusAverage',asUtility = True, n='diffNew')
        cmds.setAttr( "%s.operation" % str(diffNew), 2)
        cmds.setAttr( "%s.input3D[0].input3Dx" % str(diffNew), newMax)
        cmds.setAttr( "%s.input3D[0].input3Dy" % str(diffNew), newMax)
        cmds.setAttr( "%s.input3D[0].input3Dz" % str(diffNew), newMax)
        cmds.setAttr( "%s.input3D[1].input3Dx" % str(diffNew), newMin)
        cmds.setAttr( "%s.input3D[1].input3Dy" % str(diffNew), newMin)
        cmds.setAttr( "%s.input3D[1].input3Dz" % str(diffNew), newMin)

        diffOld = cmds.shadingNode('plusMinusAverage',asUtility = True, n='diffOld')
        cmds.setAttr( "%s.operation" % str(diffOld), 2)
        cmds.setAttr( "%s.input3D[0].input3Dx" % str(diffOld), oldMax)
        cmds.setAttr( "%s.input3D[0].input3Dy" % str(diffOld), oldMax)
        cmds.setAttr( "%s.input3D[0].input3Dz" % str(diffOld), oldMax)
        cmds.setAttr( "%s.input3D[1].input3Dx" % str(diffOld), oldMin)
        cmds.setAttr( "%s.input3D[1].input3Dy" % str(diffOld), oldMin)
        cmds.setAttr( "%s.input3D[1].input3Dz" % str(diffOld), oldMin)

        newPlusVal = cmds.shadingNode('plusMinusAverage',asUtility = True, n='newPlusVal')
        cmds.setAttr( "%s.input3D[0].input3Dx" % str(newPlusVal), newMin)
        cmds.setAttr( "%s.input3D[0].input3Dy" % str(newPlusVal), newMin)
        cmds.setAttr( "%s.input3D[0].input3Dz" % str(newPlusVal), newMin)
        
        multi = cmds.shadingNode('multiplyDivide',asUtility = True, n='multi')
        div = cmds.shadingNode('multiplyDivide',asUtility = True, n='div')
        cmds.setAttr( "%s.operation" % str(div), 2)

        #cmds.connectAttr(("%s.output3D" % str(defaultSub)), ("%s.input1" %str(multi)), force=True)
        cmds.connectAttr(("%s.output3Dx" % str(defaultSub)), ("%s.input1X" %str(multi)), force=True)
        cmds.connectAttr(("%s.output3Dy" % str(defaultSub)), ("%s.input1Y" %str(multi)), force=True)
        cmds.connectAttr(("%s.output3Dz" % str(defaultSub)), ("%s.input1Z" %str(multi)), force=True)
        cmds.connectAttr(("%s.output3D" % str(diffNew)), ("%s.input2" %str(multi)), force=True)

        #cmds.connectAttr(("%s.output" % str(multi)), ("%s.input1" %str(div)), force=True)
        cmds.connectAttr(("%s.outputX" % str(multi)), ("%s.input1X" %str(div)), force=True)
        cmds.connectAttr(("%s.outputY" % str(multi)), ("%s.input1Y" %str(div)), force=True)
        cmds.connectAttr(("%s.outputZ" % str(multi)), ("%s.input1Z" %str(div)), force=True)

        cmds.connectAttr(("%s.output3D" % str(diffOld)), ("%s.input2" %str(div)), force=True)

        cmds.connectAttr(("%s.outputX" % str(div)), ("%s.input3D[1].input3Dx" %str(newPlusVal)), force=True)
        cmds.connectAttr(("%s.outputX" % str(div)), ("%s.input3D[1].input3Dy" %str(newPlusVal)), force=True)
        cmds.connectAttr(("%s.outputX" % str(div)), ("%s.input3D[1].input3Dz" %str(newPlusVal)), force=True)



        ifBelowMin = cmds.shadingNode('condition',asUtility = True, n='ifBelowMin')
        cmds.connectAttr(refVal, ("%s.firstTerm" %str(ifBelowMin)), force=True)
        cmds.setAttr( "%s.operation" % str(ifBelowMin), 4) # lessThan
        cmds.setAttr( "%s.secondTerm" % str(ifBelowMin), oldMin)
        if v == 1:
            cmds.setAttr( "%s.colorIfTrueR" % str(ifBelowMin), newMin)
            cmds.connectAttr(("%s.output3Dx" % str(newPlusVal)), ("%s.colorIfFalseR" %str(ifBelowMin)), force=True) # plug in the new value
        else:
            cmds.setAttr( "%s.colorIfTrueR" % str(ifBelowMin), newMin)
            cmds.setAttr( "%s.colorIfTrueG" % str(ifBelowMin), newMin)
            cmds.setAttr( "%s.colorIfTrueB" % str(ifBelowMin), newMin)
            cmds.connectAttr(("%s.output3D" % str(newPlusVal)), ("%s.colorIfFalse" %str(ifBelowMin)), force=True) # plug in the new value

        ifOverMax = cmds.shadingNode('condition',asUtility = True, n='ifOverMax')
        cmds.connectAttr(("%s.outColorR" % str(ifBelowMin)), ("%s.firstTerm" %str(ifOverMax)), force=True)
        cmds.setAttr( "%s.operation" % str(ifOverMax), 2) # greaterThan
        cmds.setAttr( "%s.secondTerm" % str(ifOverMax), newMax)
        cmds.setAttr( "%s.colorIfTrueR" % str(ifOverMax), newMax)
        cmds.connectAttr(("%s.outColorR" % str(ifBelowMin)), ("%s.colorIfFalseR" %str(ifOverMax)), force=True) # plug in the new value
           
        cmds.warning('created setRange network')
        return ifOverMax

def specialToeSetup(toe,toePos,tip,tipWorld):
    # create the setup for a the sliding toe
    toe_front = toe             # the actual skinned bone
    toe_pos = toePos            # the bone serving as a position

    toe_front_helper = tip      # the bone positioned at the tip of the toe
    toe_world = tipWorld        # the bone following the tip on all axis save for Z (up)

    ntw = procNetwork()
    front_pos_vec = procNetwork().lengthVector(toe_front_helper,toe_pos) # vector between the position bone and the tip of the toe

    endNode = front_pos_vec[0]
    helperMatrix = front_pos_vec[1]
    toeMatrix = front_pos_vec[2]

    # slightly different length vector network - this one excludes the Z axis. It samples the direction in which the toe is pointing in a 2D fashion
    flatVectors = cmds.shadingNode('plusMinusAverage',asUtility = True, n='flatDirVector')
    cmds.setAttr( "%s.operation" % str(flatVectors), 2)

    cmds.connectAttr(("%s.outputTranslateX" % str(helperMatrix)), ("%s.input3D[0].input3Dx" %str(flatVectors)), force=True)
    cmds.connectAttr(("%s.outputTranslateY" % str(helperMatrix)), ("%s.input3D[0].input3Dy" %str(flatVectors)), force=True)

    cmds.connectAttr(("%s.outputTranslateX" % str(toeMatrix)), ("%s.input3D[1].input3Dx" %str(flatVectors)), force=True)
    cmds.connectAttr(("%s.outputTranslateY" % str(toeMatrix)), ("%s.input3D[1].input3Dy" %str(flatVectors)), force=True)


    flatVecLength = ntw.length(flatVectors)
    front_pos_Length = ntw.length(endNode)

    flatVec_norm = ntw.normalize(flatVecLength[1],flatVecLength[0])

    multiplyByLength = cmds.shadingNode('multiplyDivide',asUtility = True, n='multiplyLength')
    addToToePos = cmds.shadingNode('plusMinusAverage',asUtility = True, n='offsetFromToe')
    
    cmds.connectAttr(("%s.output" % str(flatVec_norm)), ("%s.input1" %str(multiplyByLength)), force=True)
    cmds.connectAttr(("%s.outputX" % str(front_pos_Length[0])), ("%s.input2X" %str(multiplyByLength)), force=True)
    cmds.connectAttr(("%s.outputX" % str(front_pos_Length[0])), ("%s.input2Y" %str(multiplyByLength)), force=True)
    cmds.connectAttr(("%s.outputX" % str(front_pos_Length[0])), ("%s.input2Z" %str(multiplyByLength)), force=True)

    cmds.connectAttr(("%s.outputTranslate" % str(toeMatrix)), ("%s.input3D[0]" %str(addToToePos)), force=True)
    cmds.connectAttr(("%s.output" % str(multiplyByLength)), ("%s.input3D[1]" %str(addToToePos)), force=True)


    cmds.connectAttr(("%s.output3Dx" % str(addToToePos)), ("%s.translateX" %str(toe_world)), force=True)
    cmds.connectAttr(("%s.output3Dy" % str(addToToePos)), ("%s.translateY" %str(toe_world)), force=True)

    ifBelowZ = cmds.shadingNode('condition',asUtility = True, n='ifBelowZ')
    
    cmds.connectAttr(("%s.outputTranslateZ" % str(helperMatrix)), ("%s.firstTerm" %str(ifBelowZ)), force=True)
    cmds.setAttr( "%s.operation" % str(ifBelowZ), 4)
    cmds.setAttr( "%s.colorIfTrueR" % str(ifBelowZ), 1)
    cmds.setAttr( "%s.colorIfFalseR" % str(ifBelowZ), 0)
    cmds.warning('created specialToeSetup')


def dotSetup(toe,toePos,tip,tipWorld):
    ntw = procNetwork()
    front_pos_vec = procNetwork().lengthVector(tip,toePos)

def vectorCurve(node,val):
    # creates a network for a vector based 'curve'
    # NOTE: the setRange in this case needs to blend between positions; this means 1 value animates 3 inputs!

    # note!!! this needs to be paired up with a SetRange of (0,nrOfPositionsToBlendTo) if you want it to work from a non-0->1 range 
    # i.e the rotation of the knee should drive a bones blending between 5 positions ==
    # knee.rot -> setRange(rotVal,0,275,0,5) -> vectorCurve(with the 5 positions selected)

    ntw = procNetwork()
    refVal = node + '.' +  val

    # the joints / locators in the selection
    sel = cmds.ls(sl=1)

    totalAdd = cmds.shadingNode('plusMinusAverage',asUtility = True, n='totalAdd')
    cmds.connectAttr( "%s.translate" % str(sel[0]), ("%s.input3D[0]" %str(totalAdd)), force=True)

    for x in range(0,len(sel)-1):
        pt0 = sel[x]
        pt1 = sel[x+1]

        # creating nodes and setting parameters
        vec = cmds.shadingNode('plusMinusAverage',asUtility = True, n='vec')
        cmds.setAttr( "%s.operation" % str(vec), 2)
        cmds.connectAttr( "%s.translate" % str(pt1), ("%s.input3D[0]" %str(vec)), force=True)
        cmds.connectAttr( "%s.translate" % str(pt0), ("%s.input3D[1]" %str(vec)), force=True)

        outR = ntw.setRange(node,val,x,x+1,0,1,v=1) # custom set range function

        multiRange = cmds.shadingNode('multiplyDivide',asUtility = True, n='multiRange')
        cmds.connectAttr( "%s.output3D" % str(vec), ("%s.input1" %str(multiRange)), force=True)
        cmds.connectAttr( "%s.outColorR" % str(outR), ("%s.input2X" %str(multiRange)), force=True)
        cmds.connectAttr( "%s.outColorR" % str(outR), ("%s.input2Y" %str(multiRange)), force=True)
        cmds.connectAttr( "%s.outColorR" % str(outR), ("%s.input2Z" %str(multiRange)), force=True)

        cmds.connectAttr( "%s.output" % str(multiRange), (("%s.input3D["+ str(x+1) + "]") %str(totalAdd)), force=True)


def IK(driverA,driverB,start=None,mid=None,end=None,pole=None,val0=0.5,val1=0.7):

    # creates a network to simulate Inverse Kinematics with only the basic operators
    # ideally includes the whole chain, both driver and driven


    # EDIT: maybe add the x1 = d-x and add the condition node so that leng>seglength doesnt pull the bone with it

    ntw = procNetwork()
    front_pos_vec = ntw.lengthVector(driverA,driverB)

    inv = cmds.shadingNode('multiplyDivide',asUtility = True, n='inv')
    cmds.connectAttr("%s.output3D" % str(front_pos_vec[0]), ("%s.input1" %str(inv)), force=True)

    flatVecLength = ntw.length(inv)
    
    d_norm = ntw.normalize(flatVecLength[1],flatVecLength[0])
    d = cmds.rename(flatVecLength[0],'d')
    print d

    d_pow = cmds.shadingNode('multiplyDivide',asUtility = True, n='d_pow')
    cmds.setAttr( "%s.operation" % str(d_pow), 3)
    cmds.setAttr( "%s.input2X" % str(d_pow), 2)

    cmds.connectAttr( "%s.outputX" % str(d), ("%s.input1X" %str(d_pow)), force=True)

    r_pow = cmds.shadingNode('multiplyDivide',asUtility = True, n='r')
    cmds.setAttr( "%s.operation" % str(r_pow), 3)
    cmds.setAttr( "%s.input1X" % str(r_pow), val0)# WARNING: temp value
    cmds.setAttr( "%s.input2X" % str(r_pow), 2)

    R_pow = cmds.shadingNode('multiplyDivide',asUtility = True, n='R')
    cmds.setAttr( "%s.operation" % str(R_pow), 3)
    cmds.setAttr( "%s.input1X" % str(R_pow), val1) # WARNING: temp value
    cmds.setAttr( "%s.input2X" % str(R_pow), 2)


    # d = length between driverA and driverB
    # r = length of bone one
    # R = length of bone two

    # X = the offset from driverA to driverB, A = the offset from X down or upwards
    # X = (d²-r²+R²) / (2*d)
    # A = ( (1/d) * sqrt( ((4*d²*R²) - (d²-r²+R²))² ) ) * 0.5
    
    # X
    multi = cmds.shadingNode('multiplyDivide',asUtility = True, n='x_multi')    
    result_X = cmds.shadingNode('multiplyDivide',asUtility = True, n='result_X')    
    cmds.setAttr( "%s.operation" % str(result_X), 2)

    minus = cmds.shadingNode('plusMinusAverage',asUtility = True, n='x_subtract')
    cmds.setAttr( "%s.operation" % str(minus), 2)
    add = cmds.shadingNode('plusMinusAverage',asUtility = True, n='x_add')

    cmds.connectAttr("%s.outputX" % str(d_pow), ("%s.input1D[0]" %str(minus)), force=True)
    cmds.connectAttr("%s.outputX" % str(r_pow), ("%s.input1D[1]" %str(minus)), force=True)
    cmds.connectAttr("%s.output1D" % str(minus), ("%s.input1D[0]" %str(add)), force=True)
    cmds.connectAttr("%s.outputX" % str(R_pow), ("%s.input1D[1]" %str(add)), force=True)

    cmds.setAttr( "%s.input1X" % str(multi), 2)
    cmds.connectAttr("%s.outputX" % str(d), ("%s.input2X" %str(multi)), force=True)

    cmds.connectAttr("%s.output1D" % str(add), ("%s.input1X" %str(result_X)), force=True)
    cmds.connectAttr("%s.outputX" % str(multi), ("%s.input2X" %str(result_X)), force=True)

    # A
    multi0 = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_multi')
    multi1 = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_multi')
    mutli2 = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_multi')
    result_A = cmds.shadingNode('multiplyDivide',asUtility = True, n='result_A')
    oneOverD = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_OneOverD')    
    cmds.setAttr( "%s.operation" % str(oneOverD), 2)

    minus = cmds.shadingNode('plusMinusAverage',asUtility = True, n='A_subtract')
    cmds.setAttr( "%s.operation" % str(minus), 2)
    add = cmds.shadingNode('plusMinusAverage',asUtility = True, n='A_add')

    pow = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_pow')
    cmds.setAttr( "%s.operation" % str(pow), 3)
    cmds.setAttr( "%s.input2X" % str(pow), 2)

    # 1 / d
    cmds.setAttr( "%s.input1X" % str(oneOverD), 1)
    cmds.connectAttr("%s.outputX" % str(d), ("%s.input2X" %str(oneOverD)), force=True)
    

    # (4*d²*R²)
    cmds.setAttr( "%s.input1X" % str(multi0), 4)
    cmds.connectAttr("%s.outputX" % str(d_pow), ("%s.input1X" %str(multi0)), force=True)

    cmds.connectAttr("%s.outputX" % str(multi0), ("%s.input1X" %str(multi1)), force=True)
    cmds.connectAttr("%s.outputX" % str(R_pow), ("%s.input2X" %str(multi1)), force=True)

    # (d²-r²+R²)
    cmds.connectAttr("%s.outputX" % str(d_pow), ("%s.input1D[0]" %str(minus)), force=True)
    cmds.connectAttr("%s.outputX" % str(R_pow), ("%s.input1D[1]" %str(minus)), force=True)
    cmds.connectAttr("%s.output1D" % str(minus), ("%s.input1D[0]" %str(add)), force=True)
    cmds.connectAttr("%s.outputX" % str(r_pow), ("%s.input1D[1]" %str(add)), force=True)
    # pow and -
    cmds.connectAttr("%s.output1D" % str(add), ("%s.input1X" %str(pow)), force=True)

    subCalc = cmds.shadingNode('plusMinusAverage',asUtility = True, n='subCalc')
    cmds.setAttr( "%s.operation" % str(subCalc), 2)

    cmds.connectAttr("%s.outputX" % str(multi1), ("%s.input1D[0]" %str(subCalc)), force=True)
    cmds.connectAttr("%s.outputX" % str(pow), ("%s.input1D[1]" %str(subCalc)), force=True)

    # subtract absolute -- is this really needed?
    absCheck = cmds.shadingNode('condition',asUtility = True, n='absCheck')
    cmds.connectAttr("%s.output1D" % str(subCalc), ("%s.firstTerm" %str(absCheck)), force=True)
    cmds.setAttr( "%s.operation" % str(absCheck), 4) # lessThan
    cmds.setAttr( "%s.secondTerm" % str(absCheck), 0.0)

    cmds.setAttr( "%s.colorIfTrueR" % str(absCheck), 0)
    cmds.setAttr( "%s.colorIfFalseR" % str(absCheck), 1)

    absMulti = cmds.shadingNode('multiplyDivide',asUtility = True, n='absMulti')
    cmds.connectAttr("%s.output1D" % str(subCalc), ("%s.input1X" %str(absMulti)), force=True)
    cmds.connectAttr("%s.outColorR" % str(absCheck), ("%s.input2X" %str(absMulti)), force=True)

    # sqrt
    sqrt = cmds.shadingNode('multiplyDivide',asUtility = True, n='sqrt')
    cmds.setAttr( "%s.operation" % str(sqrt), 3)
    cmds.setAttr( "%s.input2X" % str(sqrt), 0.5)
    cmds.connectAttr("%s.outputX" % str(absMulti), ("%s.input1X" %str(sqrt)), force=True)

    # 1/d * sqrt
    cmds.connectAttr("%s.outputX" % str(oneOverD), ("%s.input1X" %str(mutli2)), force=True)
    cmds.connectAttr("%s.outputX" % str(sqrt), ("%s.input2X" %str(mutli2)), force=True)

    # result * 0.5
    cmds.connectAttr("%s.outputX" % str(mutli2), ("%s.input1X" %str(result_A)), force=True)
    cmds.setAttr( "%s.input2X" % str(result_A), 0.5)


    # cross the vector
    vecUp = cmds.shadingNode('multiplyDivide',asUtility = True, n='up')
    cmds.setAttr( "%s.input1X" % str(vecUp), 1)
    cmds.setAttr( "%s.input1Y" % str(vecUp), 0)
    cmds.setAttr( "%s.input1Z" % str(vecUp), 0)
    cmds.setAttr( "%s.input2X" % str(vecUp), 1)
    cmds.setAttr( "%s.input2Y" % str(vecUp), 1)
    cmds.setAttr( "%s.input2Z" % str(vecUp), 1)
    cross = ntw.crossProduct(d_norm,vecUp)
    
    crossLength = ntw.length(cross)    
    cross_norm = ntw.normalize(crossLength[1],crossLength[0])

    # if d > (r+R): set A offset to 0
    absDist = cmds.shadingNode('plusMinusAverage',asUtility = True, n='absDist')
    cmds.setAttr( "%s.input1D[0]" % str(absDist), val1)
    cmds.setAttr( "%s.input1D[1]" % str(absDist), val0)

    ifDcheck = cmds.shadingNode('condition',asUtility = True, n='ifDcheck')
    cmds.connectAttr("%s.outputX" % str(d), ("%s.firstTerm" %str(ifDcheck)), force=True)
    cmds.connectAttr("%s.output1D" % str(absDist), ("%s.secondTerm" %str(ifDcheck)), force=True)
    cmds.setAttr( "%s.operation" % str(ifDcheck), 2) # greaterThan

    cmds.setAttr( "%s.colorIfTrueR" % str(ifDcheck), 0)
    cmds.setAttr( "%s.colorIfFalseR" % str(ifDcheck), 1)


    # setting up the offset from driverA
    X_normal = cmds.shadingNode('multiplyDivide',asUtility = True, n='X_normal')
    X_offset = cmds.shadingNode('plusMinusAverage',asUtility = True, n='X_offset')

    cmds.connectAttr("%s.output" % str(d_norm), ("%s.input1" %str(X_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_X), ("%s.input2X" %str(X_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_X), ("%s.input2Y" %str(X_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_X), ("%s.input2Z" %str(X_normal)), force=True)

    cmds.connectAttr("%s.outputTranslate" % str(front_pos_vec[2]), ("%s.input3D[0]" %str(X_offset)), force=True)
    cmds.connectAttr("%s.output" % str(X_normal), ("%s.input3D[1]" %str(X_offset)), force=True)


    A_normal = cmds.shadingNode('multiplyDivide',asUtility = True, n='A_normal')
    A_offset = cmds.shadingNode('plusMinusAverage',asUtility = True, n='A_offset')

    cmds.connectAttr("%s.output" % str(cross_norm), ("%s.input1" %str(A_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_A), ("%s.input2X" %str(A_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_A), ("%s.input2Y" %str(A_normal)), force=True)
    cmds.connectAttr("%s.outputX" % str(result_A), ("%s.input2Z" %str(A_normal)), force=True)

##
    distMutli = cmds.shadingNode('multiplyDivide',asUtility = True, n='distMutli')
    cmds.connectAttr("%s.output" % str(A_normal), ("%s.input1" %str(distMutli)), force=True)
    cmds.connectAttr("%s.outColorR" % str(ifDcheck), ("%s.input2X" %str(distMutli)), force=True)
    cmds.connectAttr("%s.outColorR" % str(ifDcheck), ("%s.input2Y" %str(distMutli)), force=True)
    cmds.connectAttr("%s.outColorR" % str(ifDcheck), ("%s.input2Z" %str(distMutli)), force=True)
##

    cmds.connectAttr("%s.output3D" % str(X_offset), ("%s.input3D[0]" %str(A_offset)), force=True)
    cmds.connectAttr("%s.output" % str(distMutli), ("%s.input3D[1]" %str(A_offset)), force=True)



#specialToeSetup('r_leg_foot_toe_front','r_leg_foot_toe_pos','r_leg_foot_toe_front_helper','r_leg_foot_toe_front_world')
#ntw = procNetwork()
#ntw.crossProduct('norm','decomposeMatrix8')
#sel = cmds.ls(sl=1)
#IK(sel[0],sel[1],val0=4.5,val1=6)


ntw = procNetwork()
ntw.length()
#ntw.setRange('decomposeMatrix6','outputTranslateZ',-9,175,-100,50,v=1)
#vectorCurve('l_leg_knee','rotateX')