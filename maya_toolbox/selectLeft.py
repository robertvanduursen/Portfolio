import pymel.core as pm
pm.select([jnt for jnt in pm.listRelatives(pm.ls(sl=1)[0], ad=1) if '_l_' in jnt.nodeName()])