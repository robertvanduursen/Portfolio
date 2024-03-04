import pymel.core as pm

mods = pm.getModifiers()
shift,_ctrl = False, False
if (mods & 1) > 0: shift=True
if (mods / 4 % 2) > 0: _ctrl=True


channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	#fetch maya's main channelbox
attrs = pm.channelBox(channelBox, q=True, sma=True)

sel = pm.ls(sl=1)
for ctrl in sel:
    incr = pm.currentTime(q=1)
    if _ctrl: ctrls = [ctrl.translateX,ctrl.translateY,ctrl.translateZ]
    else: ctrls = [ctrl.rotateX,ctrl.rotateY,ctrl.rotateZ]

    if attrs: ctrls = [eval('ctrl.{}'.format(attr)) for attr in attrs]


    mag = 30
    if shift: mag *= 0.5
    for attr in ctrls:
        baseVal = attr.get()
        pm.setKeyframe(attr,t=incr+0,v=baseVal)
        pm.setKeyframe(attr,t=incr+5,v=mag)
        pm.setKeyframe(attr,t=incr+10,v=baseVal)
        pm.setKeyframe(attr,t=incr+15,v=-mag)
        pm.setKeyframe(attr,t=incr+20,v=baseVal)
        incr += 20
		
    for attr in ctrls:
        pm.setKeyframe(attr,t=incr+0,v=baseVal)
        pm.setKeyframe(attr,t=incr+5,v=mag)
        pm.setKeyframe(attr,t=incr+10,v=baseVal)
        pm.setKeyframe(attr,t=incr+15,v=-mag)
        pm.setKeyframe(attr,t=incr+20,v=baseVal)
