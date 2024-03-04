pm.select(clear=1)
pm.select(pm.PyNode('Controls_Anim').listMembers())
aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
pm.currentTime(0,e=1)
pm.select(pm.PyNode('Controls_Anim').listMembers())

animCurves = []
for bit in pm.ls(sl=1):
    animCurves += [b for b in bit.inputs() if 'AnimCurve' in str(type(b)) ]

pm.delete(animCurves)
pm.select(clear=1)