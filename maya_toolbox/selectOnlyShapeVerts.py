import pymel.core as pm

x = pm.ls(sl=1)[0] # order matters
nrVerts = sum([shape.degree() + shape.spans.get() for shape in x.getShapes()])
obj = x.nodeName()+".cv[0:"+str(nrVerts)+"]"
pm.select(obj)