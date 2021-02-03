from flask import Flask, request, jsonify
from nudenet import NudeDetector
import os

app = Flask(__name__)
detector = NudeDetector()

# Image Route
@app.route('/image', methods=['POST'])
def image_detector():
    image_file = request.get_data()
    # convert binary to file path
    image_path = open('/tmp/image_file', 'wb')
    image_path.write(image_file)
    image_path.close()

    detection = detector.detect('/tmp/image_file')

    os.remove('/tmp/image_file')

    image_detection = {
        "NSFW detection": str(detection)
    }

    return image_detection

# Video Route
@app.route('/video', methods=['POST'])
def video_detector():
    video_file = request.get_data()
    # convert binary to file path
    video_path = open('/tmp/video_file', 'wb')
    video_path.write(video_file)
    video_path.close()

    detection = detector.detect_video('/tmp/video_file')

    os.remove('/tmp/videp_file')

    video_detection = {
        "NSFW detection": detection
    }

    return video_detection

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9991)