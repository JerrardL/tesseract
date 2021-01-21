from flask import Flask, request
from imageai.Detection import VideoObjectDetection
import os
import operator
from collections import OrderedDict

app = Flask(__name__)

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
execution_path = os.getcwd()
detector.setModelPath(os.path.join(execution_path, "/models/object_recognition/yolo.h5"))
detector.loadModel(detection_speed="flash")

@app.route('/', methods=['POST'])
def video_or():
    video_file = request.get_data()

    total_frequency_output = OrderedDict()

    def for_frame(frame_number, output_array, output_count):

        for key, value in output_count.items():

            if key in total_frequency_output:
                total_frequency_output[key] += int(value)
            else:
                total_frequency_output[key] = int(value)

    video_path = open('/tmp/video_file', 'wb')
    video_path.write(video_file)
    video_path.close()

    detector.detectObjectsFromVideo(input_file_path="/tmp/video_file",
                                    frames_per_second=20, log_progress=True, display_object_name=True, save_detected_video=False, per_frame_function=for_frame, thread_safe=True)

    os.remove('/tmp/video_file')

    sorted_frequency_output = sorted(
        total_frequency_output.items(), key=operator.itemgetter(1), reverse=True)

    video_or_json = {
        "Object Frequency": sorted_frequency_output
    }

    return video_or_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, threaded=False)