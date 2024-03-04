import pymel.core as pm
mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True

if shift:
	mel.eval("\
	artAttrPaintOperation artAttrSkinPaintCtx Add;\
	artAttrSkinValues artAttrSkinContext;\
	artSkinSetSelectionValue 0.02 false artAttrSkinPaintCtx artAttrSkin;\
	artAttrSkinValues artAttrSkinContext;\
	toolPropertyShow;\
	dR_updateToolSettings;"
	)
else:
	mel.eval("\
	artAttrPaintOperation artAttrSkinPaintCtx Add;\
	artAttrSkinValues artAttrSkinContext;\
	artSkinSetSelectionValue 0.1 false artAttrSkinPaintCtx artAttrSkin;\
	artAttrSkinValues artAttrSkinContext;\
	toolPropertyShow;\
	dR_updateToolSettings;"
	)