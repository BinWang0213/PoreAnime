from paraview.simple import *
import numpy as np
import sys
import os

from .filters import *

def enhanceSubVolumeEdge(input_obj,value=0):
    #Enhance sub volume edge visulization
    pore_edge,poreDisplay_edge=extractSubVolume(input_obj,None,value) #enhance visual feature
    poreDisplay_edge.SetRepresentationType('Feature Edges')
    poreDisplay_edge.Opacity=0.2
    ColorBy(poreDisplay_edge, None)

    return pore_edge,poreDisplay_edge

def FadeEffect(animationScene, input_objs_display=[], start_opacitys=[0.0],end_opacitys=[0.0], 
    vol_obj=None,vol_dataName=None,vol_opacity=[],
    nframes=25,frameID=0,saveAnimation=False,output_dir=""):
    #Fade in/out effect
    renderView = GetActiveViewOrCreate('RenderView')

    animationScene.NumberOfFrames += nframes
    for i in range(nframes):
        renderView.Update()

        for j,obj in enumerate(input_objs_display):
            change_rate=(end_opacitys[j]-start_opacitys[j])/nframes
            obj.Opacity= start_opacitys[j] + (i+1)*change_rate

        #Volume data opacity is changed by colormap
        if(vol_dataName is not None):
            velocityumsPWF = GetOpacityTransferFunction(vol_dataName)
            change_rate=(vol_opacity[1]-vol_opacity[0])/nframes
            opacity=vol_opacity[0] + (i+1)*change_rate
            velocityumsPWF.Points = [0.0, 0.0, 0.5, 0.0, 
                                    #0.5, 1.0, 0.5, 0.0,
                                    vol_obj.CellData[vol_dataName].GetRange()[1], opacity, 0.5, 0.0] 

        animationScene.GoToNext()

        if(saveAnimation):
            #Animation saving 
            image_name = os.path.join(output_dir, "%06d.png" % (frameID))
            SaveScreenshot(image_name,ImageResolution=[1920, 1080])
        
        frameID+=1
    
    return frameID


def RotateEffect(animationScene,camera_path_obj,
    nframes=25,frameID=0,saveAnimation=False,output_dir=""):
    renderView = GetActiveViewOrCreate('RenderView')

    animationScene.NumberOfFrames += nframes
    for i in range(nframes):
        renderView.Update()

        renderView.CameraPosition = camera_path_obj.interpolate_position(i, None, None, None)
        renderView.CameraFocalPoint = camera_path_obj.interpolate_focal_point(i, None, None)
        renderView.CameraViewUp = camera_path_obj.interpolate_up_vector(i, None)
        
        animationScene.GoToNext()

        if(saveAnimation):
            #Animation saving 
            image_name = os.path.join(output_dir, "%06d.png" % (frameID))
            SaveScreenshot(image_name,ImageResolution=[1920, 1080])
        
        frameID+=1

    return frameID