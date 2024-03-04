import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.mel as mel

# tool / script to work in conjunction with the 'LBG skin export / import'

# export skinning properties

text_file = open("C:\Users\gbduursr\Desktop\Output.txt", "w")

totalSel = cmds.ls(sl=1)
incrTotal = 0
for iterObj in totalSel:

    # get object
    cmds.select(iterObj)
    mSel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(mSel)

    obj = om.MObject()
    path = om.MDagPath()
    mSel.getDagPath(0,path,obj)

    # access skincluster
    sel = path.fullPathName()

    skinClus = None
    shapes = cmds.listConnections(cmds.listRelatives(sel,s=True,f=1),t='skinCluster')
    for x in shapes:
        if cmds.nodeType(x) == 'skinCluster':
            skinClus = x
            break


    if skinClus != None:
        incr = 0
        infls = cmds.skinCluster(skinClus,query=True,inf=True)
        exportString = ''
        for x in infls:

            if incr != 0:
                exportString += (',')
            exportString += x
            incr += 1

        vals = ''
        # get the skindata
        nrVrts = cmds.polyEvaluate(sel, v=True )
        for y in range(nrVrts+1):
            vertVal = cmds.skinPercent(skinClus, (sel + '.vtx['+ str(y) + ']'), query=True, value=True )

            # total weight = 1 test
            totalVal = 0.0
            for val in vertVal:
                val = round(val,2)
                totalVal += val

            if totalVal == 1.0:
                pass
            else:
                if totalVal > 1.0:
                    vertVal[len(vertVal)-1] -= round(totalVal-1.0,2)
                else:
                    vertVal[len(vertVal)-1] += round(1.0 - totalVal,2)


            vals += (str(y) + ':' + str(vertVal)[1:-1])
            if y != nrVrts:
                vals += '>'


        exportString = sel + '< ' + exportString + '<' + vals 
        if incrTotal != len(totalSel)-1:
            exportString += '\n'
        text_file.write(exportString)
        print sel + ' is exported succesfully'
    else:
        print sel + ' has no skincluster?'
    incrTotal +=1

text_file.close()
cmds.warning('EXPORT FINISHED')





#####################
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.mel as mel


exported = open("C:\Users\gbduursr\Desktop\Output.txt", "r")
for line in exported:

    # clear selection
    cmds.select(clear=1)
    newline  = line[0:-1]

    # split the line for info
    #print '           total list = ' + newline
    splitted = newline.split('<')
    obj = splitted[0]

    if cmds.objExists(obj):
         if cmds.listConnections(cmds.listRelatives(obj,s=True,f=1)[0],t='skinCluster') == None:

            infls = splitted[1]
            data = splitted[2]
            #print ' the object: ' + obj
            selectList = []
            inflList = []
            for x in infls.split(','):
                #print 'the infls = ' + x
                selectList.append(x.strip())
                inflList.append(x.strip())

            # grab the objects
            selectList.append(obj)
            #print 'the list: ' + str(selectList)
            cmds.select(selectList)
            #mel.eval("SmoothBindSkin")
            
            testClus = cmds.skinCluster(selectList, tsb=True)
            selectList = []

            # set the skin values
            # format = 0:0.0, 1.0>1:0.0, 1.0,2:0.0, 1.0
            for y in data.split('>'):
                parts = y.strip().split(':')
                #print parts[0]
                index = int(parts[0])
                skinVals = parts[1].split(',')
                skinValList = []
                incrVert = 0
                for z in skinVals:
                    skinValList.append((inflList[incrVert],round(float(z.strip()),2)))
                    incrVert +=1

                cmds.skinPercent(testClus[0], (obj + '.vtx['+ str(index) + ']'), transformValue=skinValList)


            #cmds.skinPercent( 'skinCluster1', 'pPlane1.vtx[100]', transformValue=[('joint1', 0.2), ('joint3', 0.8)])
            skinValList = []
            inflList = []
    else:
        print obj + ' does not exist in this scene'
cmds.warning('DONE')