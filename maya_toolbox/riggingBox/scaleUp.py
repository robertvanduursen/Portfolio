import pymel.core as pm
from _control_utils import *
fac = 1.5

mods = pm.getModifiers()
shift,_ctrl = False, False
if (mods & 1) > 0: shift=True
if (mods / 4 % 2) > 0: _ctrl=True

if shift: scaleShapes(1,fac,fac)
elif _ctrl: scaleShapes(fac,1,1)
else: scaleShapes(fac,fac,fac)

