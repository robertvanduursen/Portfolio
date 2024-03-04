
import fSkin as FS
reload(FS)

skins = FS.getMeshClusters()
for skin in skins:
    over = FS.isOverMaxInfluence(skin)
    if over: print skin,'= over'
