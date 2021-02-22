from flask import Flask, request, jsonify
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment

app = Flask(__name__)

r = sr.Recognizer()

@app.route('/', methods=['POST'])
def stt():
    speech = request.get_data()
    language = request.args.get('language')
    if language == None:
        language = "en-US"

    languages = language.split(sep=',')
    extractions = {}

    with sr.AudioFile(BytesIO(speech)) as source:
        audio = r.record(source)

    for lang in languages:
        # recognize speech using Sphinx
        try:
            text = r.recognize_sphinx(audio, language=lang)
        except sr.UnknownValueError:
            text = "Sphinx could not understand audio"
        except sr.RequestError as e:
            text = "Sphinx error; {0}".format(e)

        extractions[lang] = text

    return jsonify(extractions)

@app.route('/video', methods=['POST'])
def stt_video():
        video = request.get_data()
        # convert Video To Speech
        video_to_audio = AudioSegment.from_file(
        BytesIO(video), 'mp4').export(BytesIO(video), format="wav")
        video_to_audio.seek(0)
        audio = video_to_audio.read()

        #Process Speech as usual with Sphinx
        with sr.AudioFile(BytesIO(audio)) as source:
            speech = r.record(source)

        # recognize speech using Sphinx
        try:
            text = r.recognize_sphinx(speech)
        except sr.UnknownValueError:
            text = "Sphinx could not understand audio"
        except sr.RequestError as e:
            text = "Sphinx error; {0}".format(e)

        return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)