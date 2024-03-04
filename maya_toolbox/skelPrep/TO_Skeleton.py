import pymel.core as pm
import os

mayaScene = pm.sceneName()
fileName = os.path.basename(mayaScene)
filePath = os.path.dirname(mayaScene)

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True


# make sure we're in the skeleton file
if filePath.split('/')[-1].lower() == 'skeleton' and fileName.lower().startswith('skeleton_'):
	path = mayaScene.replace('/Skeleton/','/').replace('Skeleton_','Master_')
	cmds.file(path, open=True, force=shift, save=False,prompt=True)

# and toggle if we're in Skel
if filePath.split('/')[-1].lower() != 'skeleton' and fileName.lower().startswith('master_'):
	path = mayaScene.replace('/Rigging','/Rigging/Skeleton/').replace('Master_','Skeleton_')
	cmds.file(path, open=True, force=shift, save=False,prompt=True)

