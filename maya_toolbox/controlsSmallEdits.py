import pymel.core as pm
for x in pm.ls(sl=1):
    # scale the shape down relative
    piv = pm.xform(x,q=1,t=1,ws=1)
    nrVerts = sum([shape.degree() + shape.spans.get() for shape in x.getShapes()])
    obj = x.nodeName()+".cv[0:"+str(nrVerts)+"]"
    #pm.scale(obj, 0.2,0.2, 0.2 ,a=1, p=piv)
    pm.rotate(obj, 0, 0, -90, p=piv, r=1, os=1 )