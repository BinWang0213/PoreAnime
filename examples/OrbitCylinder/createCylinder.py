from paraview.simple import * 

# get active view 
renderView1 = GetActiveViewOrCreate('RenderView') 
# create a new 'Cylinder' 
cylinder1 = Cylinder(registrationName='Cylinder1')  
# show object in view 
cylinder1Display = Show(cylinder1) 
# Change properties of an object 
cylinder1.Resolution = 25
cylinder1.Height = 2.0
cylinder1.Center = [0.5, 1.0, 0.5]

cylinder1Display.SetRepresentationType('Surface With Edges')
cylinder1Display.Opacity = 0.5 

#Set up camera
renderView1.CameraPosition = [0.47, 4.81, 5.22] 
renderView1.CameraFocalPoint = [0.5, 1.0, 0.5]
renderView1.CameraViewUp = [[0.0, 1.0, 0.0]]

# Update view 
renderView1.Update()