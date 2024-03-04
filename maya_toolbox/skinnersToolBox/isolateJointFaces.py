import pymel.core as pm
from _getSkinCluster import getSkinCluster
skinClus,infls,path = getSkinCluster()

pm.skinCluster(skinClus,e=1,selectInfluenceVerts=skinClus.ptt.get())
verts = [vert for vert in pm.ls(sl=1) if 'MeshVertex' in str(type(vert))]
pm.setToolTo('selectSuperContext')
pm.select(verts)
mel.eval('ConvertSelectionToFaces')
pm.select(skinClus.ptt.get(),add=1)



isolated_panel = cmds.paneLayout('viewPanes', q=True, pane1=True)
cmds.editor( isolated_panel, edit=True, lockMainConnection=True, mainListConnection='activeList' )
cmds.isolateSelect( isolated_panel, state=1 )
