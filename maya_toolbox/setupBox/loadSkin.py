import pymel.core as pm
import Rigging.RigConstructor.lib.skinSaveLoad as skinSaveLoad
print skinSaveLoad
import os
# if SkinWeights exists: redirect
path = os.path.dirname(pm.sceneName()).replace('/','\\')+'\\'
if os.path.isdir(path + 'SkinWeights'): path += 'SkinWeights\\'

print path
skinSaveLoad.skinLoad(path)