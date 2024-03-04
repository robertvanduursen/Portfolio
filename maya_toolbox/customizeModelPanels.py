import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import pymel.core as pm
import time
from datetime import date
import datetime 

for mdlP in pm.getPanel(type='modelPanel'):
	pm.modelEditor(mdlP,e=1, locators=0)
	pm.modelEditor(mdlP,e=1, strokes=0)
	

