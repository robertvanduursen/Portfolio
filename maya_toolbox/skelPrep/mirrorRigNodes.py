import pymel.core as pm
import pymel.core.datatypes as dt


def mirrorTransform(source,target):
	#source = pm.PyNode('l_frontLeg|toeEndPos')
	#target = pm.PyNode('r_frontLeg|toeEndPos')

	# position
	mirror = dt.Matrix([-1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])
	newMatrix = source.getMatrix(worldSpace=0) * mirror
	target.setMatrix(newMatrix)

	# flip
	orig = target.getMatrix(worldSpace=0)
	mirror = dt.Matrix([-1,0,0,0,0,1,0,0,0,0,-1,0,0,0,0,1])
	newMatrix = target.getMatrix(worldSpace=0) * mirror
	newMatrix[3] = orig[3]
	target.setMatrix(newMatrix)

	# freeze
	pm.makeIdentity(target,apply=True ,scale=1)

if not pm.objExists('r_frontLeg'):
	new = pm.duplicate('l_frontLeg', rr=1, name='r_frontLeg')
	rFront = pm.PyNode('r_frontLeg')
	for locator in pm.listRelatives(rFront,c=1,type='transform'):
		lefthand = pm.PyNode(locator.longName().replace('r_frontLeg','l_frontLeg'))
		mirrorTransform(lefthand,locator)
		
if not pm.objExists('r_rearLeg'):
	new = pm.duplicate('l_rearLeg', rr=1, name='r_rearLeg')
	rFront = pm.PyNode('r_rearLeg')
	for locator in pm.listRelatives(rFront,c=1,type='transform'):
		lefthand = pm.PyNode(locator.longName().replace('r_rearLeg','l_rearLeg'))
		mirrorTransform(lefthand,locator)	
