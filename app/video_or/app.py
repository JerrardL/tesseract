from flask import Flask, request
from imageai.Detection import VideoObjectDetection
import os
import cv2
import operator
from collections import OrderedDict
from io import BytesIO

app = Flask(__name__)

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def video_or():
    video_file = request.get_data()
    execution_path = os.getcwd()

    total_unique_output = OrderedDict()

    def forFrame(frame_number, output_array, output_count):

        for key, value in output_count.items():

            if key in total_unique_output:
                total_unique_output[key] += int(value)
            else:
                total_unique_output[key] = int(value)

    video_path = open('/tmp/video_file', 'wb')
    video_path.write(video_file)
    video_path.close()

    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
    detector.loadModel()
    detector.detectObjectsFromVideo(input_file_path="/tmp/video_file",
                            frames_per_second=20, log_progress=True, display_object_name=True, save_detected_video=False, per_frame_function=forFrame)

    os.remove('/tmp/video_file')

    sorted_unique_output = sorted(total_unique_output.items(), key=operator.itemgetter(1), reverse=True)

    video_or_json = {
        "Unique Object Count": sorted_unique_output
    }

    return video_or_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181)