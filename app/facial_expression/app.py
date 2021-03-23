from flask import Flask, request, jsonify
from fer import FER
import cv2
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
if physical_devices:
  try:
    tf.config.experimental.set_virtual_device_configuration(physical_devices[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])
  except RuntimeError as e:
    print(e)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recognise():
    image_file = request.get_data()

    image_path = open('/tmp/image_file', 'wb')
    image_path.write(image_file)
    image_path.close()

    detect_img = cv2.imread('/tmp/image_file')
    detector = FER()
    detection = detector.detect_emotions(detect_img)

    results = {}
    for i, face in enumerate(detection, start=1):
        face_result = {}
        emotions = face["emotions"]
        for emotion, score in emotions.items():
            face_result[emotion] = float(score)
        results[i] = face_result
    return results

# Route for video

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8411)

