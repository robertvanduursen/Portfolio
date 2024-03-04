import pymel.core as pm
import sys
sys.path.append(r'C:\Users\rvanduursen\Desktop\EXPERIMENTS\MayaStandAloneScripts\riggingBox')
import _LM_Shapes_utils as LMS

root = pm.ls(sl=1)[0] 
ikCtrls = root.listRelatives(ad=1,type='transform')
animObjs = [node.node() for node in pm.ls('*.IsAnimationObject')]
ikCtrls = set(ikCtrls) & set(animObjs)

for ctrl in ikCtrls:
    target = pm.PyNode(ctrl.replace('ik_','fk_'))
    LMS.copyShapesToTarget(ctrl,target )