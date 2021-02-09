from flask import Flask, request
from classifier import Classifier
import os

app = Flask(__name__)
classifier = Classifier()

# Image Route
@app.route('/image', methods=['POST'])
def image_classifier():
    image_file = request.get_data()
    # convert binary to file path
    image_path = open('/tmp/image_file', 'wb')
    image_path.write(image_file)
    image_path.close()

    classification = classifier.classify('/tmp/image_file')

    os.remove('/tmp/image_file')

    nsfw_classification = {}
    _, value = next(iter(classification.items()))
    nsfw_classification["safe"] = float(value["safe"])
    nsfw_classification["unsafe"] = float(value["unsafe"])

    image_classification = {
        "prediction": nsfw_classification
    }

    return image_classification

# Video Route
@app.route('/video', methods=['POST'])
def video_classifier():
    video_file = request.get_data()
    # convert binary to file path
    video_path = open('/tmp/video_file', 'wb')
    video_path.write(video_file)
    video_path.close()

    classification = classifier.classify_video('/tmp/video_file')

    os.remove('/tmp/video_file')

    nsfw_classification = {}
    safe_total = 0 
    unsafe_total = 0
    frame_count = 0
    for _, value in classification['preds'].items():
        safe_total += float(value['safe'])
        unsafe_total += float(value['unsafe'])
        frame_count += 1
    safe_average = safe_total / frame_count
    unsafe_average = unsafe_total / frame_count
    nsfw_classification["safe average"] = safe_average
    nsfw_classification["unsafe average"] = unsafe_average

    video_classification = {
        "prediction": nsfw_classification
    }

    return video_classification

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990)