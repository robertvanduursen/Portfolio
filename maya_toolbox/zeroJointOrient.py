import pymel.core as pm
for x in pm.ls(sl=1):
	pm.makeIdentity(x,apply=True ,jointOrient=1,r=0)

