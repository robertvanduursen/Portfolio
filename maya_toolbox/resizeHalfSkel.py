import pymel.core as pm

for x in pm.listRelatives(pm.ls(sl=1)[0],ad=1,type='joint'):
    if '_l_' in x.nodeName():
        right = pm.PyNode(x.nodeName().replace('_l_','_r_'))
        right.radius.set(x.radius.get())