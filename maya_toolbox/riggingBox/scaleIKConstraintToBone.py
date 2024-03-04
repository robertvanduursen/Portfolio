import pymel.core as pm

mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True

sel = pm.ls(sl=1,type='joint')
if sel:
    sel = sel[0]
    
childJoint = sel.getParent()

pos1 = sel.getTranslation(space='world')
pos2 = childJoint.getTranslation(space='world')
mid = pos1 +( (pos2 - pos1)*0.5)
leng = (pos2 - pos1).length()

print childJoint,'->',leng

if shift: leng *= 0.5
jntConstraint = [con for con in sel.listHistory() if con.nodeType() == 'JointConstraintNode'][0]
jntConstraint.scale.set(leng)