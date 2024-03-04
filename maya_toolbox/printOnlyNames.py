import pymel.core as pm
print [str(x.nodeName()) for x in pm.ls(sl=1)]