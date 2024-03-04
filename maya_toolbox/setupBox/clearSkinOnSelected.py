import pymel.core as pm
import pymel.core.datatypes as dt

chainRoot = 'def_l_frontLegLwr_joint'
chain = [jnt for jnt in pm.listRelatives(pm.PyNode(chainRoot),ad=1) if pm.nodeType(jnt) == 'joint'] + [pm.PyNode(chainRoot)]
verts  = pm.sets('set2',q=1)
vertHook = pm.ls(verts,fl=1)[0]
pm.select(verts)

mel.eval('\
artAttrSkinToolScript 3;\
artAttrSkinJointMenu( "artJoinListPopupMenu", "artAttrSkinPaintCtx" );\
toolPropertyWindow1 ("");\
toolPropertyShow;\
dR_updateToolSettings;'
 )
 
#set the tool
mel.eval("\
artAttrPaintOperation artAttrSkinPaintCtx Replace;\
artAttrSkinValues artAttrSkinContext;\
artSkinSetSelectionValue 0.0 false artAttrSkinPaintCtx artAttrSkin;\
artAttrSkinValues artAttrSkinContext;\
toolPropertyShow;\
dR_updateToolSettings;"
)


skinClus = [con for con in vertHook.node().connections() if 'SkinCluster' in str(type(con))][0]
infls = pm.skinCluster(skinClus,q=1,inf=1)

rest = set(infls) - set(chain)
for x in rest:
    mel.eval('artSkinInflListChanging "{}" 1;'.format(x.nodeName()))
    mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
    mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`')

sink  = pm.PyNode('def_l_frontLegUprAllTwist_joint')







