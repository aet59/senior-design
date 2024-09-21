import os
import cv2
from base_camera import BaseCamera

class Camera(BaseCamera):
    # Use camera index 0 by default (usually the built-in camera)
    video_source = 0

    def __init__(self):
        # Check if there's an environment variable for the camera source 
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    # Set the camera source to a different one if needed 
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        # Open the camera using the AVFoundation backend
        camera = cv2.VideoCapture(Camera.video_source, cv2.CAP_AVFOUNDATION)
        
        # If the camera can't be opened, raise an error
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        # Capture video frames in a loop
        while True:
            success, img = camera.read()  
            if not success or img is None:
                print("Failed to capture image from camera.")
                continue  # If failed, skip this frame and try again

            # Convert the frame to JPEG format and yield it for streaming
            yield cv2.imencode('.jpg', img)[1].tobytes()





