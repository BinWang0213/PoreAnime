from paraview.simple import *
import numpy as np
import sys
import os

from .utils import *

def loadImage(fname,dataName=None,showColorBar=False):
    #Load a image from file and show it
    img = XMLImageDataReader(FileName=[fname])
    imgDisplay = Show(img)

    if(dataName is None):
        dataName=img.CellData.keys()[0] #Use the first cell data as image color

    #Set data color
    #colorData(img,imgDisplay,dataName,'CIELab Blue to Red',showColorBar)
    colorData(img,imgDisplay,dataName,'erdc_divLow_icePeach',showColorBar)

    #Set visulization type, Surface, Volume, Outline, etc
    imgDisplay.SetRepresentationType('Surface')

    # reset view to fit data bounds
    renderView = GetActiveViewOrCreate('RenderView')
    bbox,bbox_center=getDomainBbox(img)
    renderView.ResetCamera(*bbox)

    renderView.Update()

    return img,imgDisplay

def loadStreamline(fname,dataName=None,showColorBar=False):
    #Load streamline object generated from LagrangianParticleTracker
    SLs = XMLPolyDataReader(FileName=[fname])
    SLsDisplay = Show(SLs)

    if(dataName is None):
        dataName='IntegrationTime'
    
    #Show streamline
    colorData(SLs,SLsDisplay,dataName,'erdc_rainbow_dark',showColorBar)
    SLsDisplay.Opacity = 0.5

    return SLs,SLsDisplay

def loadAnimatedParticles(fname_head,numTimesteps,dataName=None,showColorBar=False):
    #Load animated particles from file
    fileList=[fname_head+str(i)+'.vtp' for i in range(numTimesteps)]
    print(fileList[0],fileList[-1])

    particle_time = XMLPolyDataReader(FileName=fileList)    
    PtsDisplay=Show(particle_time)
    PtsDisplay.SetRepresentationType('Points')
    #PtsDisplay.RenderPointsAsSpheres = 1
    #PtsDisplay.PointSize = 2.0

    if(dataName is None):
        dataName='ParticleVelocity'
    colorData(particle_time,PtsDisplay,dataName,'erdc_rainbow_dark',showColorBar)

    return particle_time,PtsDisplay

def loadAnimatedImages(fname_head,numTimesteps,dataName=None,showColorBar=False):
    #Load a image from file and show it

    fileList=[fname_head+str(i)+'.vti' for i in range(numTimesteps)]
    print(fileList[0],fileList[-1])

    img = XMLImageDataReader(FileName=fileList)
    imgDisplay = Show(img)

    if(dataName is None):
        dataName=img.CellData.keys()[0] #Use the first cell data as image color

    #Set data color
    colorData(img,imgDisplay,dataName,'X Ray',showColorBar)
    #Set visulization type, Surface, Volume, Outline, etc
    imgDisplay.SetRepresentationType('Surface')

    return img,imgDisplay