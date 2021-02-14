from paraview.simple import *
import numpy as np
import sys
import os

def getDomainBbox(input_obj):
    bbox=np.array(input_obj.GetDataInformation().DataInformation.GetBounds(),dtype=np.int32)
    bbox_center=np.mean(bbox.reshape(3,2),axis=1)
    return bbox,bbox_center


def findObject(obj_name):
    #Find the object and its corrsponding display obj
    obj=FindSource(obj_name)
    objDisplay=GetDisplayProperties(obj)
    return obj,objDisplay

def colorData(obj,obj_display,dataName,cmap='erdc_rainbow_dark',showColorBar=False):
    #Show data with a given colormap

    if(dataName in obj.PointData.keys()):
        ColorBy(obj_display, ('POINTS',dataName))
    if(dataName in obj.CellData.keys()):
        ColorBy(obj_display, ('CELLS',dataName))
    
    #Show colorbar
    renderView = GetActiveViewOrCreate('RenderView')
    if(showColorBar):
        obj_display.RescaleTransferFunctionToDataRange(True, False)
        obj_display.SetScalarBarVisibility(renderView, True)

    #Set colomap
    LUT = GetColorTransferFunction(dataName)
    LUT.ApplyPreset(cmap, True)
    PWF = GetOpacityTransferFunction(dataName)

def invertColorMap(dataName):
    #Invert Colormap 
    # get opacity transfer function/opacity map for 'MetaImage'
    metaImagePWF = GetOpacityTransferFunction(dataName)
    if(metaImagePWF.Points==[0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0]):
        metaImagePWF.Points=[0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
    else:
        metaImagePWF.Points = [0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0]