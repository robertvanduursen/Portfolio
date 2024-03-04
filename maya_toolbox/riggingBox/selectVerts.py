import pymel.core as pm

x = pm.ls(sl=1)[0]
# scale the shape down relative
piv = pm.xform(x,q=1,t=1,ws=1)
shapes = []
for shape in x.getShapes():
	nrVerts = sum([shape.degree() + shape.spans.get() ])
	shapes += [shape.nodeName()+".cv[0:"+str(nrVerts)+"]"]

#obj = x.nodeName()+".cv[0:"+str(nrVerts)+"]"
pm.select(shapes)