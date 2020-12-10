from os import getenv

from flask import Flask, request, jsonify

from .engine import SpeechToTextEngine

from pydub import AudioSegment
from io import BytesIO


MAX_ENGINE_WORKERS = int(getenv('MAX_ENGINE_WORKERS', 2))

engine = SpeechToTextEngine()

app = Flask(__name__)

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def stt():
    speech = request.get_data()
    text = engine.run(speech)
    return jsonify({"text": text})

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/video', methods=['POST'])
def convert_video():
    video = request.get_data()
    video_to_audio = AudioSegment.from_file(
        BytesIO(video), 'mp4').export(BytesIO(video), format="wav")
    video_to_audio.seek(0)
    audio = video_to_audio.read()
    text = engine.run(audio)
    return jsonify({"text": text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
