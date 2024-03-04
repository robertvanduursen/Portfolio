import pymel.core as pm

preselection = pm.ls(sl = True)
for obj in pm.selected() :
    
    jo = pm.getAttr(obj + '.jointOrient')
    pm.setAttr(obj + '.rotate', jo)
    pm.setAttr(obj + '.jointOrient', 0,0,0)
