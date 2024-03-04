import pymel.core as pm



    
	
sel = pm.ls(sl=1,flatten=1)
if all([bit for bit in sel if 'MeshVertex' in str(type(bit))]):
	verts = sel
	posList = []
	for x in verts:
		x = x.getPosition()
		if pm.currentUnit(q=1) == 'm':
		    x *= 100            
		posList.append(str((x.x,x.y,x.z)))
else:
	verts = sel[0].getPoints()
	posList = []
	for x in verts:
		if pm.currentUnit(q=1) == 'm':
			posList.append(str((x.x,x.y,x.z)))
		else:
			posList.append(str((x.x*100,x.y*100,x.z*100)))
	
command = "pm.polyCreateFacet(ch=0,tx=1,s=1,p=[{}])".format(','.join(posList))
eval(command)