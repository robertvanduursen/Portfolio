import pymel.core as pm
import maya.cmds as cmds

def getHitcheck(obj):
    for x in pm.listHistory(obj,type='polyCylinder'):
        return x

def portToMirror():
    sel = pm.ls(sl=1)[0]
    mirror = pm.ls(sel.replace('_l_','_r_'))[0] 
    
    selHit = getHitcheck(sel)
    mirrorHit = getHitcheck(mirror)
    
    mirror.translate.set(sel.translate.get())
    mirror.rotate.set(sel.rotate.get())
    
    mirrorHit.height.set(selHit.height.get())
    mirrorHit.radius.set(selHit.radius.get())

portToMirror()