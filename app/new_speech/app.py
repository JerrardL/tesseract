from flask import Flask, request, jsonify
import speech_recognition as sr
import os
from io import BytesIO

app = Flask(__name__)

r = sr.Recognizer()


@app.route('/', methods=['POST'])
def stt():
    speech = request.get_data()

    # If AudioFile needs a path:
    # speech_path = open('/tmp/speech_file', 'wb')
    # speech_path.write(speech)
    # speech_path.close()

    with sr.AudioFile(BytesIO(speech)) as source:
        audio = r.record(source)

    # recognize speech using Sphinx
    try:
        text = r.recognize_sphinx(audio, language="fr-FR")
    except sr.UnknownValueError:
        text = "Sphinx could not understand audio"
    except sr.RequestError as e:
        text = "Sphinx error; {0}".format(e)

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)