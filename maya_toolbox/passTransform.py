import pymel.core as pm

source = pm.ls(sl=1)[0]
target = pm.ls(sl=1)[1]

target.setMatrix(source.getMatrix(worldSpace=1))