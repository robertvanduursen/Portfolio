import pymel.core as pm
# rename children iteratively

base = pm.ls(sl=1)[0] 
index = False
for idx,char in enumerate(base):
    print char
    if char.isdigit():
        index = char
        break
formatName = base[:idx] +'{}'+ base[idx+1:]
index = int(index) + 1 # add 1 since enum starts @ 0
print formatName,index

skellies = [obj for obj in pm.listRelatives(base,ad=1) if obj.nodeType() == 'joint']
skellies = [bone for bone in reversed(skellies)]
for idx,bone in enumerate(skellies):
	pm.rename(bone,formatName.format(index+idx))

	
	