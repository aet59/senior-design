from flask import Flask, render_template, Response
import os

# Check if there's a specific camera set in the environment variable 'CAMERA'
# If not, use the default OpenCV camera driver
if os.environ.get('CAMERA'):
    from camera_opencv import Camera  
else:
    from camera_opencv import Camera  

# Create a Flask app
app = Flask(__name__)

@app.route('/')
# This function is linked to the homepage ('/')
# It sends the 'index.html' file, which will load the camera on the device
def index():
    return render_template('index.html')

# This function captures video frames from the camera and sends them to the webpage
def gen(camera):
    while True:
        frame = camera.get_frame()  # Get a single frame from the camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n')

@app.route('/video_feed')
# It uses the 'gen' function to send video frames to the webpage
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the app on '0.0.0.0' (makes it accessible on the network), on port 80, using threading for better performance
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
