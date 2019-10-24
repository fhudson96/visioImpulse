import numpy as np
import open3d as o3d
from open3d.open3d.geometry import voxel_down_sample
import OpenGL.GL as gl
import pangolin

class SampleToggling:
    def __init__(self):
        self.dcam = 0
        self.scam = 0
        self.zoomCoefficient = 8

    def main(self):
        '''
        Main function: Creates the user window and side bar with a button. This button is used to toggle between normal point cloud and downsampled point cloud
        '''
        pangolin.CreateWindowAndBind('Sample Toggle App', 1280, 960) #Set sindow size and name
        gl.glEnable(gl.GL_DEPTH_TEST) #This is enabled to allow for user to move/rotate 3D image with mouse

        #Define render object
        SampleToggling.scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.1, 1000),
            pangolin.ModelViewLookAt(0, 0.5, -3, 0, 0, 0, pangolin.AxisDirection.AxisY))
        handler3d = pangolin.Handler3D(SampleToggling.scam)

        #Add viewpoint object
        SampleToggling.dcam = pangolin.CreateDisplay()
        SampleToggling.dcam.SetBounds(0.0, 1.0, 180/640., 1.0, -640.0/480.0)

        SampleToggling.dcam.SetHandler(pangolin.Handler3D(SampleToggling.scam))

        #Create the side panel
        panel = pangolin.CreatePanel('buttonPanel')
        panel.SetBounds(0.0, 1.0, 0.0, 180/640.)

        gl.glPointSize(1) #Set the size of each point on the point cloud

        button = pangolin.VarBool('buttonPanel.Sampling Toggle Button', value=False, toggle=False) #Create a simple button
        
        #Read the .ply file and convert it into a numpy array so it can be understood by pangolin
        pointCloudOrigional = o3d.io.read_point_cloud("bunny.ply")
        pointCloudOrigionalArray = np.asarray(pointCloudOrigional.points)

        #Down sample this read .ply file and then convert that into a numpy array
        pointCloudDownSampled = voxel_down_sample(pointCloudOrigional, voxel_size=0.008)
        pointCloudDownSampledArray = np.asarray(pointCloudDownSampled.points)

        #Zoom the pointCloud so it is easy for user to see
        pointCloudOrigionalZoomed = pointCloudOrigionalArray * self.zoomCoefficient 
        pointCloudSampledZoomed = pointCloudDownSampledArray * self.zoomCoefficient 

        #Run a loop until the program is quit, toggling image each time button is pressed.
        while not pangolin.ShouldQuit():
            self.drawPoints(pointCloudOrigionalZoomed)
            if pangolin.Pushed(button):
                while not pangolin.Pushed(button):
                    self.drawPoints(pointCloudSampledZoomed)

    def drawPoints(self, pointCloud):
        '''
        Function to allow chosen point cloud to be drawn
        '''
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        SampleToggling.dcam.Activate(SampleToggling.scam)
        pangolin.DrawPoints(pointCloud)
        pangolin.FinishFrame()

if __name__ == '__main__':
    app = SampleToggling()
    app.main()


