import pymel.core as pm
sel = pm.ls(sl=1)
jnts = pm.ls(sel,type='joint')
geo = list(set(sel) - set(jnts))
pm.select(geo)
