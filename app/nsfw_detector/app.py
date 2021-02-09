from flask import Flask, request
from detector import Detector
import os

app = Flask(__name__)
detector = Detector()

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

    nsfw_detection = []
    for object in detection:
        data = {}
        data['label'] = object['label']
        data['probability'] = float(object['score'])
        nsfw_detection.append(data)


    image_detection = {
        "NSFW detection": nsfw_detection
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

    os.remove('/tmp/video_file')

    detected_classes = {}
    for _, value in detection['preds'].items():
        for frame in value:
            score = frame["score"]
            label = frame["label"]
            
            if label not in detected_classes:
                detected_classes[label] = {"scores": []}
            detected_classes[label]["scores"].append(score)
    
    for key, value in detected_classes.items():
        detected_classes[key]["average"] = sum(value["scores"]) / len(value["scores"])
        del detected_classes[key]["scores"]

    video_detection = {
        "NSFW detection": detected_classes
    }

    return video_detection

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9991)