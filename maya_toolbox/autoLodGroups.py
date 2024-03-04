import pymel.core as pm
# presume we have a geometry node to query in terms of LODS
'''
geoGroup = pm.PyNode('Geometry')

for obj in pm.listRelatives(geoGroup ,children=1):
    #check lods
    if '_L' in obj.nodeName():
        lodNr = obj.nodeName().split('_L')[-1]
        if not pm.objExists('Render_L'+lodNr): pm.createDisplayLayer(n='Render_L'+lodNr, empty=1)
        pm.editDisplayLayerMembers('Render_L'+lodNr, obj)    
'''		


#pm.select(pm.ls(sl=1,type='joint'))
#pm.select(pm.ls(sl=1,type='joint'))
#pm.select([x for x in pm.ls(sl=1,type='joint') if x.endswith('_end')])


for LOD in set([mesh.getTransform() for mesh in pm.ls(type='mesh')]):
    if any(LOD.nodeName().endswith(lodNr) for lodNr in ['_L0','_L1','_L2','_L3','_L4','_L5']):
        lodLayer = '_L'+LOD.nodeName().split('_L')[-1]
        pm.editDisplayLayerMembers('Render'+lodLayer, LOD)