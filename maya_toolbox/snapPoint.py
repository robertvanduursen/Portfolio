import pymel.core as pm

obj = pm.ls(sl=1)[0]
loc  =pm.spaceLocator(n='temp_'+obj.nodeName())
con = pm.parentConstraint(obj ,loc, mo=0)
pm.delete(con)
