
vert = pm.ls(sl=1)[0]
skinClus = [con for con in pm.listHistory(vert.node()) if 'SkinCluster' in str(type(con))][0]
infls = pm.skinPercent( skinClus, vert, transform=None, query=True, ignoreBelow=0.05)
infls = [pm.PyNode(jnt) for jnt in infls]
weights = pm.skinPercent( skinClus, vert, value=True, query=True, ignoreBelow=0.05)

transVals = dict(zip(infls,weights))

lefts = [side for side in infls if '_l_' in side.nodeName()]
rights = [pm.PyNode(jnt.replace('_l_','_r_')) for jnt in lefts]
center = list(set(infls) - set(lefts))

if len(infls) > 2 and len(lefts) > 1: pm.warning('the left side exceeds limit')
elif len(lefts) < 1: pm.warning('nothing to mirror')
else:
    for x in center + rights: x.lockInfluenceWeights.set(0)
    for x in lefts: x.lockInfluenceWeights.set(1)
    
    newVals = {}
    for x in rights:
        newVals[x.nodeName()] = transVals[pm.PyNode(jnt.replace('_r_','_l_'))]
    pm.skinPercent( skinClus, vert, transformValue=list(newVals.items()))


