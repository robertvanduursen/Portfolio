import pymel.core as pm

allJoints = pm.listRelatives('Skeleton',ad=1,type='joint')
defJoints = [jnt for jnt in allJoints if ('rig_' not in jnt.nodeName() and '_end' not in jnt.nodeName())]

left = [jnt for jnt in defJoints if '_l_' in jnt.nodeName()]
right = [jnt for jnt in defJoints if '_r_' in jnt.nodeName()]
center = set(defJoints) - set(right) - set(left)

for jnt in left:
    jnt.side.set(1) # left
    pm.select(jnt)
    pm.setAttr('{}.type'.format(jnt),18) # other
    label = jnt.nodeName()[6:-6]
    jnt.otherType.set(label) # left

for jnt in right:
    jnt.side.set(2) # left
    pm.select(jnt)
    pm.setAttr('{}.type'.format(jnt),18) # other
    label = jnt.nodeName()[6:-6]
    jnt.otherType.set(label) # left