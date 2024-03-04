import maya.mel as mel
import pymel.core as pm
import pymel.core.datatypes as dt

sel = pm.ls(sl=1)
joint = pm.ls(sl=1,type='joint')[0]
node = list(set(sel) - set([joint]))[0]

jointChild = joint.getChildren(type='joint')[0]
offset = (joint.getTranslation(space='world') - jointChild.getTranslation(space='world'))
size = offset.length()

shape = node.getShape()
xPos = [shape.cv[idx].getPosition()[0] for idx in range(shape.numCVs())]
scale = max(xPos) + abs(min(xPos))
resize = max(scale,size) / min(scale,size)

#node.getBoundingBox(space='world')
matrix = node.getTransformation() # worldSpace
matrix.addScale((resize,1.0,1.0),space='transform')
matrix.setTranslation(dt.Point(-min(xPos),0,0),space='object')

for idx in range(shape.numCVs()):
    pos = shape.cv[idx].getPosition()
    pos *= matrix
    newPos = dt.Point(pos[0],pos[1],pos[2])
    shape.setCV(idx,newPos)

mel.eval('doMenuNURBComponentSelection("{}", "controlVertex");'.format(node.nodeName()))
mel.eval('maintainActiveChangeSelectMode {} 0;'.format(node.nodeName()))
mel.eval('SelectTool;')




