import pymel.core as pm
pm.setToolTo('moveSuperContext')
vals = pm.manipMoveContext('Move', q=True, p=True, m=2)
mel.eval('rotate -r -p {}cm {}cm {}cm -os -fo 0 90 0'.format(vals[0],vals[1],vals[2]))