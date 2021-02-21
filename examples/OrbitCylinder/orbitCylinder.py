from paraview.simple import * 
import numpy as np

# get active view 
renderView1 = GetActiveViewOrCreate('RenderView') 

animationScene = GetAnimationScene()
animationScene.StartTime = 0
animationScene.EndTime = 1
animationScene.NumberOfFrames = 0
animationScene.PlayMode = 'Sequence'

animationScene.GoToFirst()

#Orbit around the cylinder
Initial_pos=np.array([0.47, 4.81, 5.22])
Focal_point=[0.5, 1.0, 0.5]
View_up=[0.0, 1.0, 0.0]
NumFrames=100

Orbit_center=np.array([0.5,4.81,0.5])
Orbit_raidus = np.linalg.norm(Initial_pos-Orbit_center)
Orbit_step = 2*np.pi/NumFrames

animationScene.NumberOfFrames += NumFrames
frameID=0
for i in range(NumFrames):
    renderView1.Update()

    orbit_x = Orbit_center[0]+Orbit_raidus*np.cos(i*Orbit_step)
    orbit_y = Orbit_center[1]
    orbit_z = Orbit_center[2]+Orbit_raidus*np.sin(i*Orbit_step)

    renderView1.CameraPosition = [orbit_x,orbit_y,orbit_z] 
    renderView1.CameraFocalPoint = Focal_point
    renderView1.CameraViewUp = View_up
    print(i, i*Orbit_step, renderView1.CameraPosition)

    animationScene.GoToNext()
    frameID+=1

#Sync the last Camera location to the first one
renderView1.CameraPosition = Initial_pos
renderView1.CameraFocalPoint = bbox_center
renderView1.CameraViewUp = up_vector