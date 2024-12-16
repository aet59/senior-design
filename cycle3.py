from flask import Flask, request, jsonify, render_template
import os
import base64
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = 'photos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400

        image_data = base64.b64decode(data['image'].split(',')[1])
        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        path = os.path.join(UPLOAD_FOLDER, filename)

        with open(path, 'wb') as f:
            f.write(image_data)

        return jsonify({"message": "Photo saved successfully!", "filename": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
