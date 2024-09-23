import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.OpenMayaUI as mui
import sys
import maya.cmds as cmds
maybe = cmds.myContext()
print maybe
maybe.doPress()
cmds.setToolTo(maybe)
