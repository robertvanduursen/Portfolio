# Copy FIRST Transform's shapes to ALL OTHER Shapes
import pymel.core as pm
from Rigging.RigConstructor.shapes import shapes

def copyShapesToTarget(master, slave, reselectMaster = False):
    """
    Duplicate shape nodes from the master object to the slave object, with relative transform
    :param master: pm.nt.Transform()
    :param slave: pm.nt.Transform()
    :param reselectMaster: bool() - if we are calling this from a shelf for manual shape changes, we might want to
                           reselect the master shape once we're done
    :return:
    """

    # Get all our shape objects that we want to play with
    masterShapes = master.getShapes()
    slaveShapes = slave.getShapes()
    slaveColour = shapes.getColourFromShape(slave.getShape())

    if all(isinstance(o, pm.nt.Transform) for o in [master, slave]):
        # Iterate over the shape nodes on the master object
        for shape in masterShapes:
            newShape = pm.duplicate(shape, addShape=True)[0]
            try:
                # Reconnect shader plugs because ... Maya (if it's a shape node that has a shader)
                attr, destination = newShape.instObjGroups[0].listConnections(connections=True,
                                                                              destination=True,
                                                                              plugs=True)[0]
                pm.parent(newShape, slave, relative=True, shape=True)
                pm.disconnectAttr(attr, destination)
                attr >> destination
            except IndexError:
                # Otherwise just ignore it, it's just a standalone shape
                pm.parent(newShape, slave, relative=True, shape=True)

        # Remove old shapes, and set colour of new shapes to slave shape colour
        # (so if we're copying shapes left to right, colour is preserved)
        pm.delete(slaveShapes)
        shapes.colourAllShapes(slave, slaveColour)

    if reselectMaster:
        # Reselect master object
        pm.select(master)

def copyShapesToMirror(master):
    """ copy shapes to our opposite object """
    # find our mirror
    if '_l_' in master.nodeName():
        side = '_l_'
        opp = '_r_'
    elif '_r_' in master.nodeName():
        side = '_r_'
        opp = '_l_'
    else:
        return None

    # Get the slave object
    slave = master.nodeName().replace(side, opp)
    if pm.objExists(slave):
        slave = pm.PyNode(slave)
    else:
        return None

    copyShapesToTarget(master, slave, False)

def copyShapes():
    """
    Copy shapes from first selection to selection[1:]
    if SHIFT key is selected when used, it'll copy entire selection, to opposite shapes
    :return:
    """
    copyMirror = True if pm.getModifiers() == 1 else False

    sel = pm.ls(sl=True)
    if copyMirror:
        # If we're copying to mirror
        for master in sel:
            copyShapesToMirror(master)

    elif sel.__len__() > 1:
        # If we're not copying to mirror, do all Master to Slaves
        master = sel[0]
        slave = sel[1:]
        for s in slave:
            copyShapesToTarget(master, s)