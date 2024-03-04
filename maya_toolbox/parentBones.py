import pymel.core as pm

bones = pm.ls(sl=1)
rev = [bone for bone in reversed(bones)]
for idx,bone in enumerate(rev[:-1]):
    pm.parent(bone,rev[idx+1])
    
    
    
