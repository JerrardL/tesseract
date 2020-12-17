from flask import Flask, request
from imageai.Detection import VideoObjectDetection
import os
from io import BytesIO

app = Flask(__name__)

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def video_or():
    execution_path = os.getcwd()

    total_unique_output = {}

    def forFrame(frame_number, output_array, output_count):

        for key, value in output_count.items():

            if key in total_unique_output:
                total_unique_output[key] += int(value)
            else:
                total_unique_output[key] = int(value)

        # print("FOR FRAME " , frame_number)
        # print("Output count for unique objects : ", output_count)
        # print("------------END OF A FRAME --------------")

    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
    detector.loadModel()
    video_path = detector.detectObjectsFromVideo(input_file_path="/videos/traffic-mini.mp4",
                                output_file_path="/videos/traffic_detected_new",
                                frames_per_second=20, log_progress=True, display_object_name=True, per_frame_function=forFrame)
    print(video_path)

    print("Total output count for unique objects found in video : ", total_unique_output)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)