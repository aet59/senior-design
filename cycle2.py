from flask import Flask, render_template, Response, request
import os

# Check if there's a specific camera set in the environment variable 'CAMERA'
if os.environ.get('CAMERA'):
    from camera_opencv import Camera  
else:
    from camera_opencv import Camera  
# Create a Flask app
app = Flask(__name__)


UPLOAD_FOLDER = 'uploads' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# New route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video file provided", 400

    video = request.files['video']
    video.save(os.path.join(UPLOAD_FOLDER, video.filename))  # Save video in the uploads directory
    return "Video uploaded successfully!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)


