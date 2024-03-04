
#export points to loc
text = hou.ui.readInput("Insert text")
object = "obj/geo1/" + text[1]
plane = hou.node(object)
planeGeo = plane.geometry()
points = planeGeo.iterPoints()

f = open("C:/Users/Robert/Desktop/export.model", "w")

f.write("Pt Positions")
f.write("\n")


for point in points:
    posX = point.attribValue("P")[0]
    posY = point.attribValue("P")[1]
    posZ = point.attribValue("P")[2]

    posX = round(posX,2)
    posY = round(posY,2)
    posZ = round(posZ,2)

    f.write('v '+ str(posX) + ", " + str(posY) + ", " + str(posZ) )
    f.write("\n")

f.write("prims")
f.write("\n")

for prim in planeGeo.prims():
    vrts = prim.vertices()
    f.write('pr ')
    for vtr in vrts:
        pt = vtr.point()
        f.write(str(pt.number()) + ' ')
    f.write(str(prim.isClosed()))
    f.write('\n')

f.close()