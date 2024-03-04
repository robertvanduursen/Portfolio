import pymel.core as pm
import pymel.core.datatypes as dt

chainRoot = 'def_l_frontLegLwr_joint'
chain = [jnt for jnt in pm.listRelatives(pm.PyNode(chainRoot),ad=1) if pm.nodeType(jnt) == 'joint'] + [pm.PyNode(chainRoot)]
verts  = pm.sets('set2',q=1)
vertHook = pm.ls(verts,fl=1)[0]

skinClus = [con for con in vertHook.node().connections() if 'SkinCluster' in str(type(con))][0]
infls = pm.skinCluster(skinClus,q=1,inf=1)

rest = set(infls) - set(chain)

for vert in pm.ls(verts,fl=1):
    infls = [pm.PyNode(jnt) for jnt in pm.skinPercent( skinClus, vert, transform=None, query=True, ignoreBelow=0.05)]
    rest = set(infls) - set(chain)
    if list(rest):
        print list(rest)
