# check if a context is already active, if so use that skin cluster
import pymel.core as pm
from _getSkinCluster import getSkinCluster
skinClus,infls,path = getSkinCluster()


mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True
print skinClus
if shift:
	skinClus.envelope.set(0)
	pm.warning('turn skinning OFF on'+str(pm.ls(sl=1)[0]))
else:
	
	skinClus.envelope.set(1)
	pm.warning('turn skinning ON on'+str(pm.ls(sl=1)[0]))