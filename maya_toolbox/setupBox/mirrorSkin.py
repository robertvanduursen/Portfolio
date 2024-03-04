import sys
import pymel.core as pm

sel = pm.ls(sl=1)[0]
if pm.objExists('mirrorVerts'):
	print 'active paint weights'
	mel.eval('\
	artAttrSkinToolScript 3;\
	artAttrSkinJointMenu( "artJoinListPopupMenu", "artAttrSkinPaintCtx" );\
	toolPropertyWindow1 ("");\
	toolPropertyShow;\
	dR_updateToolSettings;'
	)

	print 'lock'
	sys.path.append(r'C:\Users\rvanduursen\Desktop\EXPERIMENTS\MayaStandAloneScripts\skinnersToolBox')
	import lockAllJoints as lock
	reload(lock)
	print 'unlock'
	sys.path.append(r'C:\Users\rvanduursen\Desktop\EXPERIMENTS\MayaStandAloneScripts\skinnersToolBox')
	import unlockRight as unlockR
	reload(unlockR)

	pm.PyNode('def_c_hips_joint').liw.set(0)


	print 'set to fill'
	mel.eval("\
	artAttrPaintOperation artAttrSkinPaintCtx Replace;\
	artSkinSetSelectionValue 1.0 false artAttrSkinPaintCtx artAttrSkin;\
	artAttrSkinValues artAttrSkinContext;\
	toolPropertyShow;\
	dR_updateToolSettings;"
	 )
	 
	print 'flood fill'
	mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`')

	print 'select'
	mel.eval('select -r mirrorVerts;')
	
	print 'copy'
	mel.eval('copySkinWeights -ss  -ds  -mirrorMode YZ -surfaceAssociation closestPoint -influenceAssociation label -influenceAssociation closestJoint;')
	print 'prune'
	mel.eval('doPruneSkinClusterWeightsArgList 1 { "0.01" };')

	print 'reselect'
	pm.select(sel,r=1)
	
	mel.eval('\
	artAttrSkinToolScript 3;\
	artAttrSkinJointMenu( "artJoinListPopupMenu", "artAttrSkinPaintCtx" );\
	toolPropertyWindow1 ("");\
	toolPropertyShow;\
	dR_updateToolSettings;'
	)