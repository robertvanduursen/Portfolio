import pymel.core as pm

objs = pm.ls(sl=1,flatten=1)
pm.select(clear=1)
for obj in objs:
    jnt = pm.joint(n='vert_joint')
    pm.select(clear=1)
    jnt.translate.set(obj.getPosition())
