import pymel.core as pm

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True


cltrs = pm.ls(sl=1)
for ctrl in cltrs:
	animCurvs = [curve for curve in ctrl.listConnections() if 'animcurve' in str(type(curve)).lower()]
	pm.selectKey(clear=1)
	pm.selectKey([curve.name() for curve in animCurvs], add=1,k=1)
	scaleVal = 0.5
	if shift: scaleVal = 1.5
	pm.scaleKey(iub=False,ts=1, tp=0, fs=1, fp=0, vs=scaleVal, vp=0, animation='keys' )
