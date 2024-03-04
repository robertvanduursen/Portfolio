import pymel.core as pm

# fun exercise in functional composition?
string = 'rig_l_toeRearRing{}_end'
string = 'def_l_toeFront{}1_joint'
perm = ['Thumb','Index','Mid','Ring','Pinky']
base = pm.ls(sl=1) # order matters
for idx,bone in enumerate(base):
	pm.rename(bone,string.format(perm[idx]))