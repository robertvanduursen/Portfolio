import pymel.core as pm

objs = pm.ls(sl=1)
pm.select(clear=1)
for obj in objs:
    jnt = pm.joint(n=obj.nodeName()+'_joint')
    pm.select(clear=1)
    con = pm.parentConstraint(obj,jnt,mo=0)
    pm.delete(con)
    pm.parent(obj,jnt)
    pm.select(clear=1)
