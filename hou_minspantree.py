#min spanning

# This code is called when instances of this SOP cook.
node = hou.pwd()
defs = node.hdaModule()
geo = node.geometry()
originalPts = geo.points()

#keep only the points
for ptPos in originalPts:
    point = geo.createPoint()
    point.setPosition(ptPos.position())

#delete original geo
geo.deletePoints(originalPts)

#initiate the tree, start point is arbitrary
polyPts = geo.points()
polyTree = geo.createPolygon()
polyTree.addVertex(polyPts[0])
polyTree.setIsClosed(0)

#cast the points to a list
totalPts = list(geo.points())

while len(totalPts) > 0:

    totalPts = list(geo.points())
    pointsInTree = []

    #go through all vertices and remove the 
    for verts in geo.prims():
        for x in verts.vertices():
            if x.point() not in pointsInTree:
                pointsInTree.append(x.point())
                totalPts.pop(totalPts.index(x.point()))

    distMap = []
    distID = []
    treeID = []
    for branch in pointsInTree:
        for leaf in totalPts:
            ptDist = branch.position().distanceTo(leaf.position())
            distMap.append(ptDist)
            distID.append(leaf.number())
            treeID.append(branch.number())

    addNr = distID[distMap.index(min(distMap))]
    addBranch = treeID[distMap.index(min(distMap))]

    newBranch = geo.createPolygon()
    newBranch.addVertex(geo.points()[addBranch])
    newBranch.addVertex(geo.points()[addNr])
    newBranch.setIsClosed(0)

    totalPts.pop(totalPts.index(geo.points()[addNr]))