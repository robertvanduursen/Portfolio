import pymel.core as pm

def scaleShapes(_x,_y,_z):
	for x in pm.ls(sl=1):
		# scale the shape down relative
		piv = pm.xform(x,q=1,t=1,ws=1)
		shapes = []
		for shape in x.getShapes():
			nrVerts = sum([shape.degree() + shape.spans.get() ])
			shapes += [shape.nodeName()+".cv[0:"+str(nrVerts)+"]"]
		
		pm.scale(shapes, _x,_y,_z,a=1, p=piv)
		#pm.rotate(obj, 0, 0, -90, p=piv, r=1, os=1 )

def rotateShapes(_x,_y,_z):
	for x in pm.ls(sl=1):
		# scale the shape down relative
		piv = pm.xform(x,q=1,t=1,ws=1)
		shapes = []
		for shape in x.getShapes():
			nrVerts = sum([shape.degree() + shape.spans.get() ])
			shapes += [shape.nodeName()+".cv[0:"+str(nrVerts)+"]"]
		pm.rotate(shapes, _x,_y,_z, p=piv, r=1, os=1 )

		
def flipShapes(_x,_y,_z):
	for x in pm.ls(sl=1):
		# scale the shape down relative
		piv = pm.xform(x,q=1,t=1,ws=1)
		shapes = []
		for shape in x.getShapes():
			nrVerts = sum([shape.degree() + shape.spans.get() ])
			shapes += [shape.nodeName()+".cv[0:"+str(nrVerts)+"]"]
		pm.scale(shapes, _x,_y,_z, p=piv, r=1)