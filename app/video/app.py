from flask import Flask, request
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['POST'])
def convert_video():
    video = request.get_data()
    audio = AudioSegment.from_file(BytesIO(video), 'mp4').export(
        BytesIO(video), format="wav")
    audio.seek(0)
    return audio

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3330)
