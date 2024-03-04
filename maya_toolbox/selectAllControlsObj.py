import pymel.core as pm
controls = [obj for obj in pm.ls(l=1) if pm.attributeQuery('IsAnimationObject',node=obj,exists=1)]
print len(controls)
pm.select(controls)