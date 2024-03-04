import pymel.core as pm
pm.select([jnt for jnt in pm.ls(sl=1,type='joint') if 'rig' not in jnt.nodeName() and 'end' not in jnt.nodeName()])
