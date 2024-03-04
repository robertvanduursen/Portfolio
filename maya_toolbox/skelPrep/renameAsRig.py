import pymel.core as pm

base = pm.ls(sl=1) # order matters
for idx,bone in enumerate(base):
	newName = bone.nodeName().replace('def_','rig_')
	pm.rename(bone,newName)