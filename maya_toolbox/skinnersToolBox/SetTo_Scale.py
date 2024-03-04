import pymel.core as pm
mods = pm.getModifiers()
shift = False
if (mods & 1) > 0: shift=True

if shift:

	mel.eval("\
	artAttrPaintOperation artAttrSkinPaintCtx Scale;\
	artSkinSetSelectionValue 0.95 false artAttrSkinPaintCtx artAttrSkin;\
	artAttrSkinValues artAttrSkinContext;\
	toolPropertyShow;\
	dR_updateToolSettings;"
	 )
 
else:
	mel.eval("\
	artAttrPaintOperation artAttrSkinPaintCtx Scale;\
	artSkinSetSelectionValue 0.9 false artAttrSkinPaintCtx artAttrSkin;\
	artAttrSkinValues artAttrSkinContext;\
	toolPropertyShow;\
	dR_updateToolSettings;"
	 )