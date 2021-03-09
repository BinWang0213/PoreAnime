from paraview.simple import * 
import numpy as np


###--------------------Streamline Interpation Funcs----------------
def interp1D(time_input, Times, coord):
    interp_coord=0.0

    return interp_coord

def interpCameraPos(t, Coords, Times):
    pos=np.zeros(3)

    pos=np.array([x,y,z])
    return pos


# get active view 
renderView1 = GetActiveViewOrCreate('RenderView')


#Animator object setup
animationScene = GetAnimationScene()
animationScene.StartTime = 0
animationScene.EndTime = 1
animationScene.NumberOfFrames = 0
animationScene.PlayMode = 'Sequence'


animationScene.GoToFirst()



#Load streamline from file
data = np.load(r'E:\Code_Repos\PoreAnime\examples\CylinderFlow\trajectory.npz')
Coords=data['Coords']
Times=data['Times']


#Orbit around the cylinder
Initial_pos=Coords[0,:]
Focal_point=Coords[1,:]
View_up=[0.0, 0.0, 1.0]
NumFrames=1000

#You may need to change this to stop our streamline earlier
Total_time=Times[-1] 
Timestep=Total_time/NumFrames


animationScene.NumberOfFrames += NumFrames
frameID=0


for i in range(NumFrames-1):
    renderView1.Update()
    
    #Interpolate camera along streamline
    pos = interpCameraPos( i*Timestep, Coords, Times )
    pos_next = interpCameraPos( (i+1)*Timestep, Coords, Times )

    #focal_pos = pos_next
    focal_pos = [1.2, 0.5, 0.125]

    #Update camera parameter
    renderView1.CameraPosition = pos
    renderView1.CameraFocalPoint = focal_pos
    renderView1.CameraViewUp = View_up
    print("Iter",i,'CurrentTime', i*Timestep, pos, focal_pos)
    
    #Move to the next frame
    animationScene.GoToNext()
    frameID+=1


