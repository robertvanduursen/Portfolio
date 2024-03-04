
import pymel.core as pm

node = pm.ls(sl=1)[0]

newCam = pm.duplicate(pm.PyNode('persp'),rr=1)[0]
newGrp = pm.group(em=1)
pm.parent(newCam,newGrp)
mel.eval('lookThroughModelPanel {} modelPanel4;'.format(newCam.nodeName()))
pm.parentConstraint(node,newGrp,mo=1)

