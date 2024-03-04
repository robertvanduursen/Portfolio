import pymel.core as pm


for x in pm.ls(sl=1,fl=1):
    pos = x.getPosition(space='world')
    pos[1] = 0.0
    x.setPosition(pos,space='world')
    
mel.eval('doMenuNURBComponentSelection("{}", "controlVertex");'.format(node.nodeName()))
mel.eval('maintainActiveChangeSelectMode {} 0;'.format(node.nodeName()))
mel.eval('SelectTool;')