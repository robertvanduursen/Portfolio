import pymel.core as pm
import maya.cmds as cmds


print 'loaded'
def getSkinCluster():
	skinClus,infls,path = False,False,False
	vertSelect = False
	
	if 'MeshVertex' in str([type(sel) for sel in pm.ls(sl=1)]): vertSelect = True

	if cmds.currentCtx() == 'artAttrSkinContext':
		print 'in skin mode'
		currentPath = 'ToolSettings|MainToolSettingsLayout|tabLayout1|artAttrSkin'
		for idx,marker in enumerate(['frame','form','form','frame','form']):
			children = pm.layout(currentPath , query=True, childArray=True )
			newMarker = [x for x in children if str(marker) in x][0]
			currentPath += '|'+newMarker
		path = currentPath + '|theSkinClusterInflList'

		if vertSelect:
			print 'but vert selected'
			vert = pm.ls(sl=1)[0]
			skinClus = [con for con in pm.listHistory(vert.node()) if 'SkinCluster' in str(type(con))][0]
		else:
			skinClus = [con for con in pm.listHistory(pm.ls(sl=1)[0].getShapes()[0]) if 'SkinCluster' in str(type(con))][0]
		infls = pm.skinCluster(skinClus,q=1,inf=1)

	if cmds.currentCtx() != 'artAttrSkinContext':
		if vertSelect:
			vert = pm.ls(sl=1)[0]
			skinClus = [con for con in pm.listHistory(vert.node()) if 'SkinCluster' in str(type(con))][0]
			infls = pm.skinPercent( skinClus, vert, transform=None, query=True, ignoreBelow=0.05)
			infls = [pm.PyNode(jnt) for jnt in infls]
		else:
			skinClus = [con for con in pm.listHistory(pm.ls(sl=1)[0].getShapes()[0]) if 'SkinCluster' in str(type(con))][0]
			infls = pm.skinCluster(skinClus,q=1,inf=1)
			#locks = [cmds.skinCluster(skinClus,inf=jnt.nodeName(),q=1,lockWeights=1) for jnt in infls ]
	
	return (skinClus,infls,path)