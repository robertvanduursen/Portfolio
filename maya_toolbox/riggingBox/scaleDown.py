import pymel.core as pm
from _control_utils import *
print 'test'
fac = 0.75

mods = pm.getModifiers()
shift,_ctrl = False, False
if (mods & 1) > 0: shift=True
if (mods / 4 % 2) > 0: _ctrl=True

if shift:	
	scaleShapes(fac,1,1)
else:
	scaleShapes(fac,fac,fac)