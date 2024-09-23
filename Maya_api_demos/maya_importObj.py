import maya.cmds as cmds
import glob
import os
from fnmatch import fnmatch

multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
result = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, fileMode=3, cap="Select a folder")
path = result[0]
print path

objs = []

# imports file from a dir structure
pattern = "*.obj"

for path, subdirs, files in os.walk(path):
    for name in files:
        if fnmatch(name, pattern):
            objs.append(os.path.join(path, name))
            
print objs[0]
        
for obj in objs:
    filepath = obj;
    cmds.file(filepath,i=1)


hey = cmds.ls("*RIG*")
cmds.delete(hey)

# ==============================================================================

print path

# imports file from a dir structure
textures = []
pattern = "*.dds"

for path, subdirs, files in os.walk(result[0]):
    for name in files:
        if fnmatch(name, pattern):
           textures.append(os.path.join(path, name))
		   
transforms = cmds.ls(tr=True) #lists all the transform nodes in the scene
polyMeshes = cmds.filterExpand(transforms, sm=12 ) #filters out all the non-polymesh nodes
cmds.select(polyMeshes) #selects all the polymeshes

for mesh in polyMeshes:
	
	meshName = cmds.select(mesh)
	#get shape
	objSel = cmds.ls(sl=True, s=1, dag=1)
	
	meshName = cmds.select(mesh)
	meshSplit = cmds.ls(sl=True)[0]
	texPath = ""
	for test in textures:
		splitter = meshSplit.split('_')
		if (splitter[len(splitter)-1].lower() in str(test)):
			if("dif" in str(test)):
				texPath = test
	
	for object in objSel :
		SgNodes = cmds.listConnections(object, type='shadingEngine')
		matMaya = cmds.listConnections(SgNodes [0] + '.surfaceShader')
		objectName = object.replace('Shape', '')
		#print 'OBJECT: ' + objectName + ' | ' + 'MAYA SHADER: ' + matMaya[0] 
	
	myShader = cmds.shadingNode('file', name= "new", asTexture=True)
	cmds.setAttr( (myShader+ '.fileTextureName'), texPath, typ='string' )
	cmds.connectAttr( (myShader+'.outColor'), (matMaya[0]+'.color'), force=1)




print textures


	
	
