import pymel.core as pm

#parent to same parent
toMove = pm.ls(sl=1)[:-1]
toParentNextTo = pm.ls(sl=1)[-1]

for x in toMove:
	pm.parent(x,toParentNextTo.getParent())