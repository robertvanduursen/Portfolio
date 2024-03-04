mel.eval('\
artAttrSkinToolScript 3;\
artAttrSkinJointMenu( "artJoinListPopupMenu", "artAttrSkinPaintCtx" );\
toolPropertyWindow1 ("");\
toolPropertyShow;\
dR_updateToolSettings;'
)
mel.eval('artSkinRevealSelected artAttrSkinPaintCtx;')