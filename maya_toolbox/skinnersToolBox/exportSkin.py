import pymel.core as pm
import Rigging.RigConstructor.lib.skinSaveLoad as skinSaveLoad
print skinSaveLoad
import os
skinSaveLoad.skinSave(os.path.dirname(pm.sceneName()).replace('/','\\')+'\\')