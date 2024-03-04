import pymel.core as pm
import maya.cmds as cmds

def portToMirror():	
    for jnt in pm.ls(sl=1):
		jntConstraint = [con for con in jnt.listHistory() if con.nodeType() == 'JointConstraintNode'][0]
		mirror = pm.ls(jntConstraint.replace('_l_','_r_'))[0]

		copyAttr = ['scale','twistAxisToggle','angleTwist']
		for attr in copyAttr: eval('mirror.{}.set(jntConstraint.{}.get())'.format(attr,attr))

		invertAttr = ['rotate0','rotate1','rotate2','angleUp','angleDown','angleRight','angleLeft']
		swapDict = {
			'angleUp':'angleDown',
			'angleDown':'angleUp',
			'angleRight':'angleLeft',
			'angleLeft':'angleRight'
		}
		for attr in invertAttr:
			getAttr = attr
			if attr in swapDict.keys(): getAttr = swapDict[attr]
			val = eval('jntConstraint.{}.get()'.format(getAttr))
			
			if type(val) in [type(0),type(1.0)]:
				val *= -1.0
				#if eval('jntConstraint.{}.get()'.format(getAttr)).getMin() is not None: 					val = min(val,eval('jntConstraint.{}.get()'.format(getAttr)).getMin())
			eval('mirror.{}.set({})'.format(attr,val))
			
portToMirror()