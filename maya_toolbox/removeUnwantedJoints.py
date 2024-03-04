import pymel.core as pm
skinClus = [con for con in pm.listHistory(pm.ls(sl=1)[0].getShapes()[0]) if 'SkinCluster' in str(type(con))][0]
infls = pm.skinCluster(skinClus,q=1,inf=1)

jnts = [
'def_l_frontLegUpr_joint', 'def_r_frontLegUpr_joint', 'def_l_frontLegLwr_joint', 'def_r_frontLegLwr_joint',
'def_l_rearLegLwr_joint', 'def_r_rearLegLwr_joint', 'def_l_rearLegUpr_joint', 'def_r_rearLegUpr_joint'
 ]
for x in jnts:
    if x in infls: 
        print x,'found'
        pm.skinCluster(skinClus, e=1, ri=x)