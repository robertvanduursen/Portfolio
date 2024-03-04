import pymel.core as pm
import pymel.core.datatypes as dt


target = pm.ls(sl=1)[0]
driver = pm.PyNode(target.replace('_poseHandle','DrivenPose'))

mirror = pm.PyNode(target.replace('_l_','_r_'))
mirrorDriver = pm.PyNode(driver.replace('_l_','_r_'))

mirror.translate.set(dt.Vector(target.translate.get())*-1)
mirror.rotate.set(dt.Vector(target.rotate.get())*-1)


if round(sum(target.translate.get()),3) == 0:
	mir = dt.Vector(driver.translate.get())
	mir.x *= -1
	mirror.translate.set(mir)

#mirrorDriver.translate.set(dt.Vector(driver.translate.get())*-1)
#mirrorDriver.rotate.set(dt.Vector(driver.rotate.get())*-1)

