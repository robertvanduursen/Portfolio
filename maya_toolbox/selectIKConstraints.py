import pymel.core as pm
allJoints = pm.ls(type='joint')
ikJoints = [pm.listRelatives(jnt,ad=1,type='JointConstraintShapeNode') for jnt in allJoints]
pm.select(ikJoints)