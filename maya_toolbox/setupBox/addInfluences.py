import pymel.core as pm

sel = pm.ls(sl=1)
jnts = pm.ls(sel,type='joint')
geo = list(set(sel) - set(jnts))[0]
#pm.select(jnts)

skinClus = pm.PyNode(mel.eval('findRelatedSkinCluster {}'.format(geo.nodeName())))
print 'skinClus =',skinClus

newJnts = set(jnts) - set(pm.skinCluster(skinClus,q=1,inf=1)) 
for jnt in newJnts :
	pm.skinCluster(skinClus, e=1, ug=1, dr=4, ps=0, ns=10, lw=1, wt=0, ai=jnt)
