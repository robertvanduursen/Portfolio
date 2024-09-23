import sys, math
import maya.cmds as cmds
# NOTE: sys.float_info was added in Python 2.6
# We hackishly append an attribute here for Maya 2009 and older
try: sys.float_info
except:
    class SysFloatInfoAttribute:
        epsilon = 2.2204460492503131e-16
    sys.float_info = SysFloatInfoAttribute()
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx

# NODES TO ADD
# NULL node!!
# constant node!!

# vector length
# cross
# dot
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_normalizeNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_norm'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033777)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'vec'
    kInput1AttrLongName = 'vector'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'normVec'
    kOutputAttrLongName = 'normalVector'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_normalizeNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_normalizeNode.input1Attr))
            input1 = dataHandle.asDouble3()
            output = om.MVector(input1[0],input1[1],input1[2])
            output.normalize()

            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_normalizeNode.outputAttr))
            dataHandle.set3Double(output.x,output.y,output.z)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.k3Double )
        nAttr.setKeyable(True)
        nAttr.setReadable(True)

        nAttr2 = om.MFnNumericAttribute()
        cls.outputAttr = nAttr2.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Double)
        nAttr2.setWritable(False)
        nAttr2.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_pointNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_pointvec'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033665)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'vec0'
    kInput1AttrLongName = 'vector0'

    input2Attr = None
    kInput2AttrName = 'vec1'
    kInput2AttrLongName = 'vector1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'outVec'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_pointNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_pointNode.input1Attr))
            input1 = dataHandle.asDouble3()
            vec0 = om.MVector(input1[0],input1[1],input1[2])

            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_pointNode.input2Attr))
            input2 = dataHandle.asDouble3()
            vec1 = om.MVector(input2[0],input2[1],input2[2])
            # compute output
            output = om.MVector((vec0 - vec1))
            output.normalize()

            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_pointNode.outputAttr))
            dataHandle.set3Double(output.x,output.y,output.z)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.k3Double )
        nAttr.setKeyable(True)
        nAttr.setReadable(True)

        nAttr1 = om.MFnNumericAttribute()
        cls.input2Attr = nAttr1.create(cls.kInput2AttrLongName, cls.kInput2AttrName, om.MFnNumericData.k3Double)
        nAttr1.setKeyable(True)
        # ouput attributes
        # output number

        nAttr2 = om.MFnNumericAttribute()
        cls.outputAttr = nAttr2.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Double)
        nAttr2.setWritable(False)
        nAttr2.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_curveNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_curve'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033745)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'

    input2Attr = None
    kInput2AttrName = 'in2'
    kInput2AttrLongName = 'input2'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_curveNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_curveNode.input1Attr))
            dataHandle.geometryTransformMatrix()
            curveObj = om.MFnNurbsCurve(dataHandle.asNurbsCurve())

            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_curveNode.input2Attr))
            input2 = dataHandle.asDouble()
            # compute output
            temp = om.MPoint()

            # clamp
            pt = max(min(input2, curveObj.length()), 0.0)
            
            curveObj.getPointAtParam(pt,temp,om.MSpace.kWorld)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_curveNode.outputAttr))
            dataHandle.set3Double(temp.x,temp.y,temp.z)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnTypedAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNurbsCurveData.kNurbsCurve )
        nAttr.setKeyable(True)
        nAttr.setReadable(True)

        nAttr1 = om.MFnNumericAttribute()
        cls.input2Attr = nAttr1.create(cls.kInput2AttrLongName, cls.kInput2AttrName, om.MFnNumericData.kDouble)
        nAttr1.setKeyable(True)
        # ouput attributes
        # output number

        nAttr2 = om.MFnNumericAttribute()
        cls.outputAttr = nAttr2.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Double)
        nAttr2.setWritable(False)
        nAttr2.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_maxNode(ommpx.MPxNode):
    """
    A node to compute the maximum of all connected inputs
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_Max'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00031321)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the and input 2."""
        if (plug == RVD_maxNode.outputAttr):
            # get the incoming data
            arrayDataHandle = om.MArrayDataHandle(dataBlock.inputValue(RVD_maxNode.input1Attr))
            # compute output
            output = 0.0
            try: output = (arrayDataHandle.inputValue()).asDouble()
            except: pass
            for i in range(arrayDataHandle.elementCount()-1):
                arrayDataHandle.next()
                output = max(output,(arrayDataHandle.inputValue()).asDouble())
            """
            # an alternative approach using an MPlug; less efficient because MPlug is slower
            arrayPlug = om.MPlug(self.thisMObject(), AR_AverageArrayDoublesNode.input1Attr)
            output = 0.0
            for i in range(arrayPlug.numElements()):
                elementPlug = om.MPlug(arrayPlug[i]).asDouble() # index operator works with physical indices
                output += elementPlug.asDouble()
            try: output /= arrayPlug.numElements()
            except: pass
            """
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_maxNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)#kDoubleArray
        nAttr.setKeyable(True)
        nAttr.setArray(True)
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnNumericAttribute.kDelete)
        # ouput attributes
        # output number
        nAttr1 = om.MFnNumericAttribute()
        cls.outputAttr = nAttr1.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr1.setWritable(False)
        nAttr1.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)

        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_SineNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_Sine'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033329)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_SineNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_SineNode.input1Attr))
            input1 = dataHandle.asDouble()
            # compute output
            output = math.sin(input1)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_SineNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)

        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_CosineNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_Cos'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033249)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_CosineNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_CosineNode.input1Attr))
            input1 = dataHandle.asDouble()
            # compute output
            output = math.cos(input1)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_CosineNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)

        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_RadToDegNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_RadToDeg'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033749)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_RadToDegNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_RadToDegNode.input1Attr))
            input1 = dataHandle.asDouble()
            # compute output
            output = math.degrees(input1)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_RadToDegNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)

        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_DegToRadNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_degToRad'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00038749)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_DegToRadNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_DegToRadNode.input1Attr))
            input1 = dataHandle.asDouble()
            # compute output
            output = math.radians(input1)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_DegToRadNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)

        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_PowNode(ommpx.MPxNode):
	"""
	A node to compute the arithmetic mean of two doubles.
	"""
	## the name of the nodeType
	kPluginNodeTypeName = 'rvd_Pow'
	## the unique MTypeId for the node
	kPluginNodeId = om.MTypeId(0x00041329)
	
	# input attributes
	## first input number
	input1Attr = None
	kInput1AttrName = 'in1'
	kInput1AttrLongName = 'input1'
	input2Attr = None
	kInput2AttrName = 'in2'
	kInput2AttrLongName = 'input2'
	
	# output attributes
	## the arithmetic mean of in1 and in2
	output = None
	kOutputAttrName = 'out'
	kOutputAttrLongName = 'output'
	
	def __init__(self):
		ommpx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		"""Compute the arithmetic mean of input 1 and input 2."""
		if (plug == RVD_PowNode.outputAttr):
			# get the incoming data
			dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_PowNode.input1Attr))
			input1 = dataHandle.asDouble()
			dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_PowNode.input2Attr))
			input2 = dataHandle.asDouble()
			# compute output
			output = math.pow(input1,input2)
			# set the outgoing plug
			dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_PowNode.outputAttr))
			dataHandle.setDouble(output)
			dataBlock.setClean(plug)
		else: return om.kUnknownParameter
	
	@classmethod
	def nodeCreator(cls):
		return ommpx.asMPxPtr(cls())
	
	@classmethod
	def nodeInitializer(cls):
		# input attributes
		# first input number
		nAttr = om.MFnNumericAttribute()
		cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
		nAttr.setKeyable(True)
		cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName, om.MFnNumericData.kDouble)
		nAttr.setKeyable(True)
		# ouput attributes
		# output number
		cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
		nAttr.setWritable(False)
		nAttr.setStorable(False)
		
		# add the attributes
		cls.addAttribute(cls.input1Attr)
		cls.addAttribute(cls.input2Attr)
		
		cls.addAttribute(cls.outputAttr)
		
		# establish effects on output
		cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_ModNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_Mod'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033327)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    ## second input number
    input2Attr = None
    kInput2AttrName = 'in2'
    kInput2AttrLongName = 'input2'
	
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_ModNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_ModNode.input1Attr))
            input1 = dataHandle.asDouble()
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_ModNode.input2Attr))
            input2 = dataHandle.asDouble()
            # compute output
            output = input1%input2
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_ModNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
		# second input number
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_arcCosNode(ommpx.MPxNode):
	"""
	A node to compute the arithmetic mean of two doubles.
	"""
	## the name of the nodeType
	kPluginNodeTypeName = 'rvd_Acos'
	## the unique MTypeId for the node
	kPluginNodeId = om.MTypeId(0x00042329)
	
	# input attributes
	## first input number
	input1Attr = None
	kInput1AttrName = 'in1'
	kInput1AttrLongName = 'input1'
	
	# output attributes
	## the arithmetic mean of in1 and in2
	output = None
	kOutputAttrName = 'out'
	kOutputAttrLongName = 'output'
	
	def __init__(self):
		ommpx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		"""Compute the arithmetic mean of input 1 and input 2."""
		if (plug == RVD_arcCosNode.outputAttr):
			# get the incoming data
			dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_arcCosNode.input1Attr))
			input1 = dataHandle.asDouble()
			# compute output
			output = math.acos(input1)
			# set the outgoing plug
			dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_arcCosNode.outputAttr))
			dataHandle.setDouble(output)
			dataBlock.setClean(plug)
		else: return om.kUnknownParameter
	
	@classmethod
	def nodeCreator(cls):
		return ommpx.asMPxPtr(cls())
	
	@classmethod
	def nodeInitializer(cls):
		# input attributes
		# first input number
		nAttr = om.MFnNumericAttribute()
		cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
		nAttr.setKeyable(True)
		# ouput attributes
		# output number
		cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
		nAttr.setWritable(False)
		nAttr.setStorable(False)
		
		# add the attributes
		cls.addAttribute(cls.input1Attr)
		
		cls.addAttribute(cls.outputAttr)
		
		# establish effects on output
		cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class matrixComponent(ommpx.MPxNode):
	"""
	A node to compute the arithmetic mean of two doubles.
	"""
	## the name of the nodeType
	kPluginNodeTypeName = 'rvd_mtrxComp'
	## the unique MTypeId for the node
	kPluginNodeId = om.MTypeId(0x00045229)
	
	# input attributes
	## first input number
	input1Attr = None
	enumer = None
	kInput1AttrName = 'in1'
	kInput1AttrLongName = 'inMatrix'
	
	# output attributes
	## the arithmetic mean of in1 and in2
	output = None
	kOutputAttrName = 'out'
	kOutputAttrLongName = 'out_Vec'
	
	def __init__(self):
		ommpx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		"""Compute the arithmetic mean of input 1 and input 2."""
		if (plug == matrixComponent.outputAttr):
			# get the incoming data
			dataHandle = om.MDataHandle(dataBlock.inputValue(matrixComponent.input1Attr))
			input1 = dataHandle.asMatrix()
			# compute output
			dataHandle = om.MDataHandle(dataBlock.inputValue(matrixComponent.enumer))
			select = dataHandle.asShort()

			# set the outgoing plug
			dataHandle = om.MDataHandle(dataBlock.outputValue(matrixComponent.outputAttr))
			if select == 0:
				dataHandle.set3Double(input1(0,0),input1(0,1),input1(0,2))
			if select == 1:
				dataHandle.set3Double(input1(1,0),input1(1,1),input1(1,2))
			if select == 2:
				dataHandle.set3Double(input1(2,0),input1(2,1),input1(2,2))
			dataBlock.setClean(plug)
		else: return om.kUnknownParameter
	
	@classmethod
	def nodeCreator(cls):
		return ommpx.asMPxPtr(cls())
	
	@classmethod
	def nodeInitializer(cls):
		# input attributes
		# first input number
		nAttr = om.MFnMatrixAttribute ()
		cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName)
		nAttr.setKeyable(True)

		#enum attr
		enumAttr = om.MFnEnumAttribute()
		cls.enumer = enumAttr.create("vectorComp", "vc", 0)
		enumAttr.addField("X", 0)
		enumAttr.addField("Y", 1)
		enumAttr.addField("Z", 2)
		enumAttr.setKeyable(True)
		enumAttr.setReadable(True)

		# ouput attributes
		# output number
		nAttr1 = om.MFnNumericAttribute()
		cls.outputAttr = nAttr1.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Double)
		nAttr1.setWritable(False)
		nAttr1.setStorable(False)
		
		# add the attributes
		cls.addAttribute(cls.input1Attr)
		cls.addAttribute(cls.enumer)
		cls.addAttribute(cls.outputAttr)
		
		# establish effects on output
		cls.attributeAffects(cls.input1Attr, cls.outputAttr)
# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class RVD_arcSineNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'rvd_Asin'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00042429)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == RVD_arcSineNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(RVD_arcSineNode.input1Attr))
            input1 = dataHandle.asDouble()
            # compute output
            output = math.asin(input1)
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(RVD_arcSineNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
# -----------------------------------------------------------------------------
# Initialize
# -----------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj, 'Robert van Duursen', '2.0', 'Any')
    try:
        plugin.registerNode(RVD_SineNode.kPluginNodeTypeName, RVD_SineNode.kPluginNodeId, RVD_SineNode.nodeCreator, RVD_SineNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_SineNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_ModNode.kPluginNodeTypeName, RVD_ModNode.kPluginNodeId, RVD_ModNode.nodeCreator, RVD_ModNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_ModNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_PowNode.kPluginNodeTypeName, RVD_PowNode.kPluginNodeId, RVD_PowNode.nodeCreator, RVD_PowNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_PowNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_arcCosNode.kPluginNodeTypeName, RVD_arcCosNode.kPluginNodeId, RVD_arcCosNode.nodeCreator, RVD_arcCosNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_arcCosNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_CosineNode.kPluginNodeTypeName, RVD_CosineNode.kPluginNodeId, RVD_CosineNode.nodeCreator, RVD_CosineNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_CosineNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(matrixComponent.kPluginNodeTypeName, matrixComponent.kPluginNodeId, matrixComponent.nodeCreator, matrixComponent.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%matrixComponent.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_arcSineNode.kPluginNodeTypeName, RVD_arcSineNode.kPluginNodeId, RVD_arcSineNode.nodeCreator, RVD_arcSineNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_arcSineNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_RadToDegNode.kPluginNodeTypeName, RVD_RadToDegNode.kPluginNodeId, RVD_RadToDegNode.nodeCreator, RVD_RadToDegNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_RadToDegNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_DegToRadNode.kPluginNodeTypeName, RVD_DegToRadNode.kPluginNodeId, RVD_DegToRadNode.nodeCreator, RVD_DegToRadNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_DegToRadNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_maxNode.kPluginNodeTypeName, RVD_maxNode.kPluginNodeId, RVD_maxNode.nodeCreator, RVD_maxNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_maxNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_curveNode.kPluginNodeTypeName, RVD_curveNode.kPluginNodeId, RVD_curveNode.nodeCreator, RVD_curveNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_curveNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_pointNode.kPluginNodeTypeName, RVD_pointNode.kPluginNodeId, RVD_pointNode.nodeCreator, RVD_pointNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_pointNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(RVD_normalizeNode.kPluginNodeTypeName, RVD_normalizeNode.kPluginNodeId, RVD_normalizeNode.nodeCreator, RVD_normalizeNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%RVD_normalizeNode.kPluginNodeTypeName)
# -----------------------------------------------------------------------------
# Uninitialize
# -----------------------------------------------------------------------------
def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(RVD_SineNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_SineNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_ModNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_ModNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_PowNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_PowNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_arcCosNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_arcCosNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_CosineNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_CosineNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(matrixComponent.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%matrixComponent.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_arcSineNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_arcSineNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_RadToDegNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_RadToDegNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_DegToRadNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_DegToRadNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_maxNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_maxNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_curveNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_curveNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_pointNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_pointNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(RVD_normalizeNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%RVD_normalizeNode.kPluginNodeTypeName)