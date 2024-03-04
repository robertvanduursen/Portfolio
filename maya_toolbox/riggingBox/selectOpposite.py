# Select Opposite, hold 'shift' to add to selection
import pymel.core as pm
if pm.getModifiers() == 1:
    add = True
else:
    add = False

sel = pm.ls(sl=True)
centreObjects = [o for o in sel if not any(i in o.name() for i in ['_l_', '_r_'])]

pm.select(clear=True)

sideObjects=[]
for o in [x for x in sel if x not in centreObjects]:
    side, opposite = ('_r_', '_l_') if '_r_' in o.name().lower() else ('_l_', '_r_') if '_l_' in o.name().lower() else (None, None)
    if side:
        sideObjects.append(pm.PyNode(o.name().replace(side, opposite)))
allObjects = sideObjects+centreObjects
if add:
    allObjects = sel + allObjects

pm.select(allObjects)