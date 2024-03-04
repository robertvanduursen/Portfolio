import pymel.core as pm
import os


# make sure we're in the skeleton file
scenePath = pm.sceneName()
if os.path.basename(scenePath).lower().startswith('master_'):
    repath = scenePath.replace('Master_','Test_')
    cmds.file(rn=repath)
    cmds.file(save=1,f=1)

scenePath = pm.sceneName()
if os.path.basename(scenePath).lower().startswith('test_'):

	skelGrp = pm.PyNode('Skeleton')
	jointCildren = skelGrp.listRelatives(ad=1,type='joint')
	nonJointChildren = set(skelGrp.listRelatives(ad=1)) - set(jointCildren)
	pm.delete(nonJointChildren)

	for jnt in jointCildren:
		jnt.translate.disconnect()
		jnt.rotate.disconnect()
		
	ControlsGrp = pm.PyNode('Controls')
	pm.select(ControlsGrp.listRelatives(ad=1))
	pm.select(ControlsGrp,add=1)
	pm.lockNode(lock=0)
	pm.delete('Controls')

	pm.delete('RigBuilder')

	mel.eval('layerEditorSelectUnused;layerEditorDeleteLayer ""')

	for jnt in jointCildren:
		pm.setKeyframe(jnt.translate)
		pm.setKeyframe(jnt.rotate)
