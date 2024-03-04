import pymel.core as pm
import maya.cmds as cmds

def getHitcheck(obj):
    children = pm.listRelatives(obj,c=1,type='transform') 
    for child in children:
        for x in pm.listHistory(child,type='polyCylinder'):
            return x
    

sel = pm.ls(sl=1,type='joint')
if sel:
    sel = sel[0]
childJoint = [jnt for jnt in pm.listRelatives(sel,c=1,type='joint') if 'twist' not in jnt][0]
print childJoint

pos1 = sel.getTranslation(space='world')
pos2 = childJoint.getTranslation(space='world')
mid = pos1 +( (pos2 - pos1)*0.5)
leng = (pos2 - pos1).length()

parentSpace = pos1

hit = getHitcheck(sel)
hit.height.set(leng*0.5)
hitcheckTrans = pm.listConnections(hit)[0]
pm.parent(hitcheckTrans,w=1) # lol local space sillyness
hitcheckTrans.translate.set(mid) 
pm.parent(hitcheckTrans,sel)