import pymel.core as pm
import Rigging.RigConstructor.lib.skinSaveLoad as skinSaveLoad
print skinSaveLoad
import os

mayaScene = pm.sceneName()
fileName = os.path.basename(mayaScene)
filePath = os.path.dirname(mayaScene)

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True


# if in HalfSkel
if 'halfskel' in fileName.lower():
	path = mayaScene.replace('HalfSkel_','Skeleton_')
	cmds.file(path, open=True, force=shift, save=False,prompt=True)
else:
	path = mayaScene.replace('Skeleton_','HalfSkel_')
	cmds.file(path, open=True, force=shift, save=False,prompt=True)




