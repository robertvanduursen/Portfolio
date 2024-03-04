# this test executed on 80,000 vertices sphere and 6 faces box
from time import time
from maya import OpenMaya as om
import pymel.core as pm
from pymel.core import *
import math


def calc_time(f):
    def fn(*args, **kwargs):
        s = time()
        r = f(*args, **kwargs)
        e = time()
        print('[TIME] %f sec' % (e - s))
        return r

    return fn


import pymel.core as pm
import pymel.core.datatypes as dt
import math


def angleMe(vec1,vec2): return math.degrees(vec1.angle(vec2))


# [TIME] 1.117000 sec
# 57.1 times faster than pymel version of it!!
@calc_time
def om_calliper(sample,refPt):
    pos = refPt.getMatrix()[3][:-1]
    refVec = om.MVector(pos[0],pos[1],pos[2])
    d = api.toMDagPath(sample.nodeName())
    d.extendToShape()
    dmfn = om.MFnMesh(d)
    s = om.MSpace.kWorld
    pts = om.MPointArray()
    dmfn.getPoints(pts, s)
    p = om.MPoint()

    # get center
    for i in xrange(pts.length()): p += om.MVector(pts[i])
    center = om.MVector(p.x / pts.length(), p.y / pts.length(), p.z / pts.length())


    loc = pm.spaceLocator(n='midOfPts')
    loc.translate.set(center)

    # do the calliper
    farhtestPt = False
    farhtest = 0.00
    for i in xrange(pts.length()):
        # get farthest
        leng = (refVec - om.MVector(pts[i])).length()
        if leng > farhtest:
            farhtest = leng
            farhtestPt = pts[i]

    if farhtestPt:
        farPt = farhtestPt
        farhtestPt = False
        farhtest = 0.00
        for i in xrange(pts.length()):
            if pts[i] != farPt:
                # get farthest
                leng = (om.MVector(farPt) - om.MVector(pts[i])).length()
                if leng > farhtest:
                    farhtest = leng
                    farhtestPt = pts[i]

        loc = pm.spaceLocator(n='farthestFromRoot')
        loc.translate.set(farPt)

        loc = pm.spaceLocator(n='farthestFromFarthest')
        loc.translate.set(farhtestPt)


#om_calliper(pm.ls(sl=1)[0],refPt=pm.ls(sl=1)[1])



@calc_time
def om_spaceExtend(sample,refPt):
    """ finds the farhtest points in the sameple relative to the reference point """
    pos = refPt.getMatrix()[3][:-1]
    refVec = om.MVector(pos[0],pos[1],pos[2])
    d = api.toMDagPath(sample.nodeName())
    d.extendToShape()
    dmfn = om.MFnMesh(d)
    s = om.MSpace.kWorld
    pts = om.MPointArray()
    dmfn.getPoints(pts, s)
    p = om.MPoint()

    down = om.MVector(0,1,0)

    # find farthest dot
    farhtestPt = False
    farhtest = 1.00
    for i in xrange(pts.length()):
        # get farthest

        vec = (om.MVector(pts[i])- refVec)
        dot = (down * vec.normal())

        if dot < farhtest:
            farhtest = dot
            farhtestPt = pts[i]


    # if found; find the one is opposite side / half of space
    if farhtestPt:
        loc = pm.spaceLocator(n='farthestFromRoot')
        loc.translate.set(farhtestPt)
        newPt = farhtestPt
        # repeat, cos if correct, the farhest dot from the farhest point relative to the root is the opposite of a natural maximum walking arm
        # i.e. if a animal swings its legs, the extends of that space should describe an biggest arc
        newVec = (om.MVector(farhtestPt) - refVec).normal()

        farhtestPt = False
        farhtest = 1.0
        for i in xrange(pts.length()):
            # get farthest
            vec = (om.MVector(pts[i]) - refVec)
            dot = (newVec * vec.normal())

            if dot < farhtest:
                farhtest = dot
                farhtestPt = pts[i]

        backVec = (om.MVector(farhtestPt) - down).normal()

        loc = pm.spaceLocator(n='farthestFromFarthest')
        loc.translate.set(farhtestPt)

        pm.curve(d=1,p=[(farhtestPt.x,farhtestPt.y,farhtestPt.z), (newPt.x,newPt.y,newPt.z)])

        print 'front =',angleMe(down,newVec)
        print 'back =', angleMe(down, backVec)



#om_spaceExtend(pm.ls(sl=1)[0],refPt=pm.ls(sl=1)[1])

@calc_time
def om_closestPoint(sample,refPt):
    """ finds the farhtest points in the sameple relative to the reference point """
    pos = refPt.getMatrix()[3][:-1]
    refVec = om.MVector(pos[0],pos[1],pos[2])
    d = api.toMDagPath(sample.nodeName())
    d.extendToShape()
    dmfn = om.MFnMesh(d)
    s = om.MSpace.kWorld
    pts = om.MPointArray()
    dmfn.getPoints(pts, s)
    p = om.MPoint()

    down = om.MVector(0,1,0)

    # find farthest dot
    farhtestPt = False
    farhtest = 10000000000000.00
    for i in xrange(pts.length()):
        # get farthest

        vec = (om.MVector(pts[i])- refVec).length()
        if vec < farhtest:
            farhtest = vec
            farhtestPt = pts[i]


    # if found; find the one is opposite side / half of space
    if farhtestPt:
        loc = pm.spaceLocator(n='closestToRoot')
        loc.translate.set(farhtestPt)



#om_closestPoint(pm.ls(sl=1)[0],refPt=pm.ls(sl=1)[1])

def getMiddle(curve,mesh,refPt):
    """ get the middle of the curve, get cross product relative to ref point and get highest dot """
    pos = refPt.getMatrix()[3][:-1]
    refVec = om.MVector(pos[0],pos[1],pos[2])

    d = api.toMDagPath(curve.nodeName())
    d.extendToShape()
    fnCurve = om.MFnNurbsCurve(d)

    d = api.toMDagPath(mesh.nodeName())
    d.extendToShape()
    dmfn = om.MFnMesh(d)


    pt1,pt2 = om.MPoint(),om.MPoint()
    fnCurve.getCV(0,pt1,om.MSpace.kWorld)
    fnCurve.getCV(1, pt2, om.MSpace.kWorld)

    pt1 = om.MVector(pt1)
    pt2 = om.MVector(pt2)

    mid = pt2 + ((pt1 - pt2) * 0.5)
    midToRef = (mid - refVec) # normal from one end to the other
    crossed = midToRef.normal() ^ (pt1 - pt2).normal()

    #upVec =
    #downVec =
    # place the mid point on tangent with ref point
    tangentPt = pt2 + ((pt1 - pt2) * (1-((pt1 - pt2).normal() * (refVec - pt2).normal()))) # the proper mid point
    loc = pm.spaceLocator(n='tangent')
    loc.translate.set(tangentPt)

    """
    pts = om.MPointArray()
    dmfn.getPoints(pts, om.MSpace.kWorld)

    loc = pm.spaceLocator(n='mid')
    loc.translate.set(mid)

    # do a 2D dot sum
    farhtestPt = False
    farhtest = 1.00
    for i in xrange(pts.length()):
        # get farthest
        
        vec = (om.MVector(pts[i])- refVec)
        dot1 = (crossed * vec.normal())
        dot2 = (midToRef.normal() * vec.normal())
        finalDot = dot1 + dot2

        if 0 < finalDot < farhtest:
            farhtest = finalDot
            farhtestPt = pts[i]

    loc = pm.spaceLocator(n='crossUp')
    loc.translate.set(farhtestPt)

    invCrossed = crossed * -1
    farhtestPt = False
    farhtest = 1.00
    for i in xrange(pts.length()):
        # get farthest

        vec = (om.MVector(pts[i]) - refVec)
        dot1 = (invCrossed * vec.normal())
        dot2 = (midToRef.normal() * vec.normal())
        finalDot = dot1 + dot2

        if 0 < finalDot < farhtest:
            farhtest = finalDot
            farhtestPt = pts[i]

    loc = pm.spaceLocator(n='crossDown')
    loc.translate.set(farhtestPt)
    """

#getMiddle(pm.ls(sl=1)[0],pm.ls(sl=1)[1],refPt=pm.ls(sl=1)[2])



def positionCylinder():
    """ get the middle of the curve, get cross product relative to ref point and get highest dot """
    verts = pm.ls(sl=1, flatten=1)
    # check if selecion is already verts
    posList = [om.MVector(x.getPosition()) for x in verts]

    mid = om.MVector(0,0,0)
    for x in posList:
        mid += x
    mid /= len(posList)
    print mid.x,mid.y,mid.z

    loc = pm.spaceLocator(a=True)
    loc.translate.set([mid.x,mid.y,mid.z])

    # build the dot products, based off a rotating constant, get the best pair
    bestPair = False
    bestDist = 0.0
    steps = 20.0
    portion = (math.pi*2) / steps
    for incr in range(int(steps)):
        print portion*incr

        constant = om.MVector(math.sin(portion*incr),0,math.cos(portion*incr)) # a flat one
        centerDots = [(idx,(mid-x).normal() * constant)  for idx,x in enumerate(posList)]
        best = sorted(centerDots,key= lambda x: x[1])
        best2 = [best[0],best[-1]]
        print best2
        dist = (posList[best[0][0]] - posList[best[-1][0]]).length()
        if dist > bestDist:
            bestDist = dist
            bestPair = best2

    loc = pm.spaceLocator(a=True)
    first = posList[bestPair[0][0]]
    loc.translate.set([first .x,first .y,first .z])
    loc = pm.spaceLocator(a=True)
    first = posList[bestPair[1][0]]
    loc.translate.set([first.x, first.y, first.z])


#positionCylinder()

def fitEllipsoid():
    """ get the middle of the curve, get cross product relative to ref point and get highest dot """
    verts = pm.ls(sl=1, flatten=1)
    # check if selecion is already verts
    posList = [om.MVector(x.getPosition()) for x in verts]

    xPos = [x[0] for x in posList]
    w  = float(sum(xPos)) / max(len(xPos), 1)
    yPos = [x[1] for x in posList]
    y  = float(sum(yPos)) / max(len(yPos), 1)
    zPos = [x[2] for x in posList]
    z  = float(sum(zPos)) / max(len(zPos), 1)


    '''
    import pymel.core as pm

    box = pm.exactWorldBoundingBox(pm.ls(sl=1,fl=1))
    
    _x = min(box[0],box[3]) + ((max(box[0],box[3]) - min(box[0],box[3])) * 0.5)
    _y = min(box[1],box[4]) + ((max(box[1],box[4]) - min(box[1],box[4])) * 0.5)
    _z  = min(box[2],box[5]) + ((max(box[2],box[5]) - min(box[2],box[5])) * 0.5)
    
    loc = pm.spaceLocator(a=True,n='mids')
    loc.translate.set([_x,_y,_z])
    '''

    mid = om.MVector(w,y,z)
    mid = om.MVector(0, 0, 0)
    for x in posList:
        mid += x
    mid /= len(posList)
    #print mid.x,mid.y,mid.z

    loc = pm.spaceLocator(a=True,n='mid')
    loc.translate.set([mid.x,mid.y,mid.z])

    # build the dot products, based off a rotating constant, get the best pair
    bestPair = False
    bestDist = 0.0
    steps = 20.0
    portion = (math.pi*2) / steps
    for incr in range(int(steps)):
        print portion*incr

        constant = om.MVector(math.sin(portion*incr),0,math.cos(portion*incr)) # a flat one
        centerDots = [(idx,(mid-x).normal() * constant)  for idx,x in enumerate(posList)]
        best = sorted(centerDots,key= lambda x: x[1])
        best2 = [best[0],best[-1]]
        print best2
        dist = (posList[best[0][0]] - posList[best[-1][0]]).length()
        if dist > bestDist:
            bestDist = dist
            bestPair = best2

    loc = pm.spaceLocator(a=True)
    first = posList[bestPair[0][0]]
    loc.translate.set([first .x,first .y,first .z])
    loc = pm.spaceLocator(a=True)
    first = posList[bestPair[1][0]]
    loc.translate.set([first.x, first.y, first.z])


fitEllipsoid()