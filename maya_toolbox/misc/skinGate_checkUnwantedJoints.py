import pymel.core as pm


physBones= pm.ls(sl=1)
rest = pm.ls(sl=1)
nonLeafs = [r for r in rest if len([x for x in r.getChildren(type='joint') if not '_end' in x.nodeName() and not 'rig' in x.nodeName()])]
pm.select(set(nonLeafs) - set(physBones))