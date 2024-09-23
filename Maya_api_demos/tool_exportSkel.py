import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import sys
import maya.cmds as cmds


root = cmds.ls(sl=1)[0]
# go through heirarchy and create a dictonary
children = cmds.listRelatives(root, ad=1)
children.insert(0,root)

skelDict = {}
skelDict[0] = root
incr = 1

f = open("C:/Users/Robert/Desktop/skel.txt", "w")

for child in children:
    path = cmds.ls(child,l=1)[0]
    index = len(path.split('|'))-2
    parent = None
    if index > 0:
    	parent = '|'.join(path.split('|')[0:-1])
    name = child
    # X, Y, Z pos + scalars
    # use unique path for duplicate names

    # note: this returns the relative matrix
    matrix = cmds.xform(path,q=True,matrix=True)
    vec_X = (matrix[0],matrix[1],matrix[2])
    vec_Y = (matrix[4],matrix[5],matrix[6])
    vec_Z = (matrix[8],matrix[9],matrix[10])
    pos = (matrix[12],matrix[13],matrix[14])

    worldPos = cmds.xform(path,q=True,ws=True,a=True,t=True)
    pos = (worldPos[0],worldPos[1],worldPos[2])

    skelDict[incr] = [name,path,index,vec_X,vec_Y,vec_Z,pos]

    X_string  = str(vec_X[0]) + "," + str(vec_X[1]) + "," + str(vec_X[2])
    Y_string  = str(vec_Y[0]) + "," + str(vec_Y[1]) + "," + str(vec_Y[2])
    Z_string  = str(vec_Z[0]) + "," + str(vec_Z[1]) + "," + str(vec_Z[2])
    pos_string = str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2])

    f.write(str(incr) + "#" + str(child) + "#" + X_string + "#" + Y_string + "#" + Z_string + "#" + pos_string + "#" + str(index) + "#" + str(parent) + "#" + path)
    f.write("\n")

    incr += 1

f.close()
# build dict from heirarchy (ideal frozen joints)
# position
# orientation
# heirarchy (parenting & index)
# limits


#f.write("Light Positions")
#f.write("\n")