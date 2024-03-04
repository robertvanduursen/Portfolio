import maya.cmds as cmds
import math

# scripts to align the bbox's of objs
class vector3():
    local = [0.0,0.0,0.0]
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.local = [x,y,z]
        pass

    def __getitem__(self,i):
        return self.local[i]

    def __setitem__(self,i,y):
        self.local[i] = y

    def __sub__(x,y):
        tempX = x[0] - y[0]
        tempY = x[1] - y[1]
        tempZ = x[2] - y[2]
        return vector3(tempX,tempY,tempZ)

    def __add__(x,y):
        tempX = x[0] + y[0]
        tempY = x[1] + y[1]
        tempZ = x[2] + y[2]
        return vector3(tempX,tempY,tempZ)

    def length(self):
        x = self.local[0]
        y = self.local[1]
        z = self.local[2]
        summed = math.pow(x,2) + math.pow(y,2) + math.pow(z,2)
        return math.sqrt(summed)

    def norm(self):
        leng = self.length()
        x = self.local[0]
        y = self.local[1]
        z = self.local[2]
        return vector3(x/leng,y/leng,z/leng)

    def cross(self,x):
        return 'not yet implemented'

    def dot(self,x):
        return 'not yet implemented'

    def toStr(self):
        return self.local
