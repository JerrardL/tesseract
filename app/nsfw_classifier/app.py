from flask import Flask, request, jsonify
from nudenet import NudeClassifier
import os

app = Flask(__name__)
classifier = NudeClassifier()

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

# Video Route -- TO BE CONFIGURED
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
    for _, value in classification.items():
        nsfw_classification["safe"] = float(value["safe"])
        nsfw_classification["unsafe"] = float(value["unsafe"])

    video_classification = {
        "prediction": nsfw_classification
    }

    return video_classification

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990)