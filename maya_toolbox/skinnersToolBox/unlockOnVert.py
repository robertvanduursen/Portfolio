import pymel.core as pm
from _getSkinCluster import getSkinCluster
skinClus,infls,path = getSkinCluster()

[jnt.liw.set(0) for jnt in infls ]
#[pm.treeView(path, e=1, image=(jnt,1,"Lock_OFF.png")) for jnt in infls]