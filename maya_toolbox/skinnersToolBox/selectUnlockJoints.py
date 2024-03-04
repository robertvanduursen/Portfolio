import pymel.core as pm
from _getSkinCluster import getSkinCluster
skinClus,infls,path = getSkinCluster()

pm.select([jnt for jnt in infls if jnt.liw.get() == 0])
