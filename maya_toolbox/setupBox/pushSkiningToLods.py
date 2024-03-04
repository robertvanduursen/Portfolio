import maya.cmds as cmds
from pymel import core as pm

import SkinWrap    
import fSetMaxInfluences as fMax

# do the skinWrap based on available matching geo objects. i.e. AF02_Legs_L0 -> AF02_Legs_L5
topGroup = pm.ls(sl=1)[0]
lodGroups = pm.listRelatives(topGroup,c=1,s=0)

topLod = False
for grp in lodGroups:
    if 'L0' in grp.nodeName() :
        topLod = grp
print topLod

otherGroups = list(set(lodGroups) - set([topLod]))
L0_geo = pm.listRelatives(topLod,c=1,s=0)

LODredux = { # lodlevel: nrMaxInfl,prune level
    1: (4,0.01),
    2: (3,0.02),
    3: (2,0.02),
    4: (1,0.02),
    5: (1,0.02),
    6: (1,0.02)
}

for LOD in otherGroups:
    LODlevel = eval(LOD.split('_L')[-1])
    LOD_geo = pm.listRelatives(LOD,c=1,s=0)
    
    # for every model present in the LOD group: skinWrap if there is a matching model in the L0 group
    for geo in LOD_geo:
        for match in L0_geo:
            #print 'trying to match',geo.nodeName()[:-1],'to', match.nodeName()[:-1]
            if geo.nodeName()[:-1] == match.nodeName()[:-1]:
                # match found: do skinWrap
                pm.select([match,geo])
                #print pm.ls(sl=1), 'selected and trying to skinWrap'
                scpt = SkinWrap.MainScript() 
                scpt.Start()

                #print 'match',geo
                pm.select(geo)
                fMax.setMaxInfluences(maxInfs=LODredux[LODlevel][0])


pm.select(topLod)
