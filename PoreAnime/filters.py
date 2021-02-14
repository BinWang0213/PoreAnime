from paraview.simple import *
import numpy as np
import sys
import os

def extractSubVolume(input_obj,dataName=None,value=0):
    #Extract sub-volume from image by its scalar value
    vol = Threshold(Input=input_obj)
    if(dataName is None):
        dataName=input_obj.CellData.keys()[0] #Use the first cell data as image color
    
    vol.Scalars = ['CELLS', dataName]
    vol.ThresholdRange = [value, value] # Assume 1.0 is rock
    volDisplay = Show(vol)
    volDisplay.SetRepresentationType('Surface')
    return vol,volDisplay




def createFastCutter(input_obj, renderView):
   #One layer subset is much faster than default slicer in Paraview
   extractSubset1 = ExtractSubset(Input=input_obj)
   extractSubset1Display = Show(extractSubset1, renderView, 'UniformGridRepresentation')
   extractSubset1Display.SetRepresentationType('Surface')
   renderView.Update()
   return extractSubset1,extractSubset1Display

def createFastSliceObject(input_obj, renderView, plane="XY"):
    #Convert a solid object into shell for faster slicing

    if(plane=="XY"): clipNormal=[0.0,0.0,1.0]
    if(plane=="YZ"): clipNormal=[1.0,0.0,0.0]
    if(plane=="XZ"): clipNormal=[0.0,1.0,0.0]

    Hide(input_obj)
    rockSurface = ExtractSurface(Input=input_obj)
    rockSurfaceDisplay = Show(rockSurface)
    rockSurfaceDisplay.SetRepresentationType('Surface')
    renderView.Update()

    Hide(rockSurface)
    clip1 = Clip(Input=rockSurface)
    clip1.ClipType = 'Plane'
    clip1.Scalars = ['CELLS', 'MetaImage']
    clip1.Value = 1.0
    # init the 'Plane' selected for 'ClipType'
    clip1.Crinkleclip = 0
    clip1.ClipType.Normal = clipNormal

    Hide3DWidgets(proxy=clip1.ClipType)

    clip1Display = Show(clip1)
    clip1Display.SetRepresentationType('Surface')

    renderView.Update()
    return clip1,clip1Display
    

def setSliceLoc(slicer,bbox,plane="XY",loc=0):
   #Set slicer location
   VOI=np.array(bbox)
   if(plane=="XY"): 
      VOI[4],VOI[5]=loc,min(bbox[5],(loc+1))
   if(plane=="XZ"): 
      VOI[2],VOI[3]=loc,min(bbox[3],(loc+1))
   if(plane=="YZ"): 
      VOI[0],VOI[1]=loc,min(bbox[1],(loc+1))
   slicer.VOI = VOI

def setCliperRange(cliper,bbox,plane="XY",loc_range=[0,1]):
   #Set cliper range
   VOI=np.array(bbox)
   if(plane=="XY"): 
      VOI[4],VOI[5]=max(bbox[4],loc_range[0]),min(bbox[5],loc_range[1])
   if(plane=="XZ"): 
      VOI[2],VOI[3]=max(bbox[2],loc_range[0]),min(bbox[3],loc_range[1])
   if(plane=="YZ"): 
      VOI[0],VOI[1]=max(bbox[0],loc_range[0]),min(bbox[1],loc_range[1])
   cliper.VOI = VOI

def interpPlaneLoc(i,imax,bbox,plane="XY",inverse=False):
   #Interpolate relative plane location in a bbox by given i in [0,imax]
   if(plane=="XY"): box_max = bbox[5]
   if(plane=="XZ"): box_max = bbox[3]
   if(plane=="YZ"): box_max = bbox[1]
   
   slice_I=int(i/imax * box_max)
   if(inverse): slice_I=box_max-slice_I
   return slice_I



