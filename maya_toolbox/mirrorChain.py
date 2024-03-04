import pymel.core as pm
import pymel.core.datatypes as dt

# reorient the right foot with the same orientation as the left but mirrored only on the Z axis
if len(pm.ls(sl=1)) > 1:
    jnts = pm.ls(sl=1)
else:
    jnts = [jnt for jnt in pm.listRelatives(pm.ls(sl=1)[0], ad=1)] + [pm.ls(sl=1)[0]]


for jnt in jnts:
    jnt.parent = jnt.getParent()  # remember the parents to put it back together later
    pm.parent(jnt, w=1)  # unparent all joints to make them world space transforms


rightJnts = []
for oldJnt in jnts:
    # make the mirrored joint (can be duplicated if there are bits you want to copy across)
    pm.select(clear=1)
    newJnt = pm.joint(n=oldJnt.replace('_l_', '_r_'))
    newJnt.parent = oldJnt.parent.replace('_l_', '_r_')

    # flip it across to the other side
    leftMatrix = oldJnt.getMatrix(worldSpace=1)
    mirrorMtrx = dt.Matrix([-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0])
    newMatrix = leftMatrix * mirrorMtrx.inverse()
    newJnt.setMatrix(newMatrix)
    pm.makeIdentity(newJnt, apply=1, r=1, s=1)

    # if the Y axis is facing Up; ignore the rotate below!
    if (dt.Vector(dt.Matrix(newJnt.getMatrix(worldSpace=1))[1][:-1]) * dt.Vector(0,1,0)) < 0.8:
        # now 'rotate' it 180 around the X axis
        oriMatrix = dt.Matrix(newJnt.getMatrix(worldSpace=1))  # recast to prevent editing the reference
        oriMatrix[2] = [bit * -1 for bit in oriMatrix[2]]
        oriMatrix[1] = [bit * -1 for bit in oriMatrix[1]]
        newJnt.setMatrix(oriMatrix)
        pm.makeIdentity(newJnt, apply=1, r=1, s=1)

    rightJnts.append(newJnt)

pm.select(clear=1)
#reparent the bones back to their original heirarchy
for jnt in jnts + rightJnts:
    pm.parent(jnt, jnt.parent)
    pm.makeIdentity(jnt, apply=1, r=1)
