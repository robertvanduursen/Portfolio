import pymel.core as pm
allJoints = [x.node() for x in pm.ls('*.IsAnimationObject')]
pm.select(allJoints)
