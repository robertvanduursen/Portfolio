# check if a context is already active, if so use that skin cluster
import pymel.core as pm
from _getSkinCluster import getSkinCluster


if all([True if obj.nodeType() == 'joint' else False for obj in pm.ls(sl=1)]):
	infls = pm.ls(sl=1)
else:
	skinClus,infls,path = getSkinCluster()

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True

print path
#locks = [cmds.skinCluster(skinClus,inf=jnt.nodeName(),q=1,lockWeights=1) for jnt in infls ]

if shift:
	[jnt.liw.set(0) for jnt in infls ]
	if path: [pm.treeView(path, e=1, image=(jnt,1,"Lock_OFF.png")) for jnt in infls]
	
	pm.warning('unlocked all joints on'+str(pm.ls(sl=1)[0]))
	
else:
	[jnt.liw.set(1) for jnt in infls ]
	if path: [pm.treeView(path, e=1, image=(jnt,1,"Lock_ON.png")) for jnt in infls]

	pm.warning('lock all joints on'+str(pm.ls(sl=1)[0]))