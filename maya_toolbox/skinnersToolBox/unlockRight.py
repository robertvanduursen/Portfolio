# check if a context is already active, if so use that skin cluster
import pymel.core as pm
from _getSkinCluster import getSkinCluster
skinClus,infls,path = getSkinCluster()

infls = [infl for infl in infls if '_r_' in infl.nodeName()]

[jnt.liw.set(0) for jnt in infls ]
[pm.treeView(path, e=1, image=(jnt,1,"Lock_OFF.png")) for jnt in infls]


pm.warning('unlock all joints on'+str(pm.ls(sl=1)[0]))