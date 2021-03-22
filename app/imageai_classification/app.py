from flask import Flask, request
from imageai.Detection import ObjectDetection
import os
import operator
from collections import OrderedDict
import json
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
with open("/config.json") as config_file:
    config = json.load(config_file)

ai_config = config["enrichments"]["VideoOR"]

app = Flask(__name__)

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
execution_path = os.getcwd()
detector.setModelPath(os.path.join(execution_path, "/models/object_recognition/yolo.h5"))
detector.loadModel(detection_speed=ai_config["detection_speed"])

@app.route('/', methods=['POST'])
def classify():
    image_file = request.get_data()

    total_output = OrderedDict()
    output_count = {}

    image_path = open('/tmp/image_file', 'wb')
    image_path.write(image_file)
    image_path.close()

    _, detection = detector.detectObjectsFromImage(input_image="/tmp/image_file", output_type="array", thread_safe=True)

    os.remove('/tmp/image_file')

    for object in detection:
            output_count[object["name"]] = object["percentage_probability"]

    def unique_count(output_count):
        for key, value in output_count.items():
            if key in total_output:
                total_output[key] += int(value)
            else:
                total_output[key] = int(value)
        sorted_output = sorted(total_output.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_output

    classification_json = {
        "Object Found, Percentage Probability": unique_count(output_count)
    }

    return classification_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7711, threaded=False)