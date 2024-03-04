import pymel.core as pm
import pymel.core.datatypes as dt

for target in pm.ls(sl=1):
	driver = pm.PyNode(target.replace('_poseHandle','DrivenPose'))

	target.translate.set(dt.Vector(driver.translate.get())*-1)
	target.rotate.set(dt.Vector(driver.rotate.get())*-1)

