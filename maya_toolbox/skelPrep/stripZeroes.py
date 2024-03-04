import pymel.core as pm
for x in pm.ls(sl=1): pm.rename(x,x.nodeName().replace('0',''))