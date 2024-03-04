import pymel.core as pm

for obj in pm.ls(sl=1):
    oldParent = obj.getParent()
    oldName = obj.nodeName()
    loc = pm.spaceLocator()
    con = pm.parentConstraint(obj,loc,mo=0)
    pm.delete(con,obj)
    
    pm.parent(loc,oldParent)
    pm.rename(loc,oldName )