import pymel.core as pm
pm.setToolTo('moveSuperContext')
vals = pm.manipMoveContext('Move', q=True, p=True, m=2)

if pm.currentUnit(q=1) == 'cm'
	vals = [val*100 for val in vals]


#print vals
mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True

if shift:
	pm.select(clear=1)
	loc = pm.joint()
else:
	loc = pm.spaceLocator(a=True)
	

loc.translate.set(vals)
#cmds.xform(loc, cp=True)
