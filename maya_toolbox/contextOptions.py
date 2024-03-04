
	
import pymel.core as pm
sel = cmds.ls(sl=1)
pm.addAttr(sel[0], longName='rigSectionRoot', at="bool")

for obj in cmds.ls(sl=1):
    pm.addAttr(obj, longName='contextOptions', dt="string", keyable=True)
    pm.setAttr(obj+'.contextOptions', 'E>Select Rig>selectAllRig')