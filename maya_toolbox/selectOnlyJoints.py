import pymel.core as pm

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True
	
if not shift:
	pm.select(pm.ls(sl=1,type='joint'))
else:
	pm.select([f for f in pm.ls(sl=1) if f.nodeType() != 'joint'])