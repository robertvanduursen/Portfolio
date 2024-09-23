node = hou.pwd()
geo = node.geometry()
from math import *
# Add code to modify contents of geo.
# Use drop down menu to select examples.

geo.addAttrib(hou.attribType.Global,"feedback","")
geo.setGlobalAttribValue("feedback",str(10))


readPath = "C:/Users/Robert/Desktop/skel.txt"
ins = open(readPath, "r" )

textDict = {}
lineNr = 0
for line in ins.readlines():
        textDict[lineNr] = line
        lineNr += 1

geo.addAttrib(hou.attribType.Point,"name","")
geo.addAttrib(hou.attribType.Point,"vec_X",hou.Vector3())
geo.addAttrib(hou.attribType.Point,"vec_Y",hou.Vector3())
geo.addAttrib(hou.attribType.Point,"vec_Z",hou.Vector3())
geo.addAttrib(hou.attribType.Point,"pos",hou.Vector3())
geo.addAttrib(hou.attribType.Point,"index",0)
geo.addAttrib(hou.attribType.Point,"parent","")
geo.addAttrib(hou.attribType.Point,"path","")
#geo.addAttrib(hou.attribType.Point,"test",0.0)


incr = 0.0
for element in textDict.values():

    info = element.split('#')
    idx = 0
    v_x  = info[2].split(',')
    v_y  = info[3].split(',')
    v_z  = info[4].split(',')
    pos  = info[5].split(',')
    
    newPt = geo.createPoint()
    newPt.setAttribValue('name',info[1])
    newPt.setAttribValue('vec_X',(float(v_x[0]),float(v_x[1]),float(v_x[2])))
    newPt.setAttribValue('vec_Y',(float(v_y[0]),float(v_y[1]),float(v_y[2])))
    newPt.setAttribValue('vec_Z',(float(v_z[0]),float(v_z[1]),float(v_z[2])))
    newPt.setAttribValue('pos',(float(pos[0]),float(pos[1]),float(pos[2])))
    newPt.setAttribValue('parent',info[7].strip())
    newPt.setAttribValue('path',info[8].strip())
    
    newPt.setPosition((float(pos[0]),float(pos[1]),float(pos[2])))
    incr += 1.0
    
for vert in geo.points():
    parent = None
    vertList = list(geo.points())
    vertList.pop(vertList.index(vert))
    
    for x in vertList:
        if x.attribValue('path') == vert.attribValue('parent'):
            parent = x
            newPoly = geo.createPolygon()
            newPoly.addVertex(vert)
            newPoly.addVertex(x)
            newPoly.setIsClosed(0)
