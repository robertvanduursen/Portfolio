import pymel.core as pm
import maya.cmds as cmds
import pymel.core.datatypes as dt

vert = pm.ls(sl=1)[0]
skinClus = [con for con in pm.listHistory(vert.node()) if 'SkinCluster' in str(type(con))][0]
infls = pm.skinPercent( skinClus, vert, transform=None, query=True, ignoreBelow=0.05)
infls = [pm.PyNode(jnt) for jnt in infls]
			
for jnt in infls:
	jntPos = jnt.getTranslation(space='world')
	dist = (dt.Vector(vert.getPosition(space='world')) - dt.Vector(jntPos)).length()
	sphere = pm.sphere(r=dist)[0]
	sphere.translate.set(jntPos)