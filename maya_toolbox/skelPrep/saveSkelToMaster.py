import pymel.core as pm
import os


import tortoiseSVN

# this should query, really
#tortoiseSVN.lock("scenename", closeonend=2)

# make sure we're in the skeleton file
scenePath = pm.sceneName()
if os.path.dirname(scenePath).split('/')[-1].lower() == 'skeleton':
    if os.path.basename(scenePath).lower().startswith('skeleton_'):
        #saving as masterfile
        if os.path.exists(scenePath ): pass # ask for override
        repath = scenePath.replace('/Skeleton/','/').replace('Skeleton_','Master_')# go one up (I know, dirty, but works if consistent)
        cmds.file(rn=repath)
        cmds.file(save=1,f=1)
        #repath = repath.replace('.ma','_mirSkel.ma')# save a duplicate as a mirrored skel version for easy rebuilt
        #cmds.file(rn=repath)
        #cmds.file(save=1,f=1)

cmds.file(rn=scenePath)
cmds.file(save=1,f=1)
