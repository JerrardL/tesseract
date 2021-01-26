from flask import Flask, request, jsonify
import speech_recognition as sr
import os
from io import BytesIO

app = Flask(__name__)

r = sr.Recognizer()


@app.route('/', methods=['POST'])
def stt():
    speech = request.get_data()

    with sr.AudioFile(BytesIO(speech)) as source:
        audio = r.record(source)

    # recognize speech using Sphinx
    try:
        text = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        text = "Sphinx could not understand audio"
    except sr.RequestError as e:
        text = "Sphinx error; {0}".format(e)

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)


# new-speech - intended to replace Speech enrichment.
# Works well and seemingly faster than DeepSpeech.
# Uses CMU Sphinx which includes models for other languages.
# Issue is than language must be specified first before CMU Sphinx
# uses that model to transcribe the audio.
# Is there any way to detect a langauge from audio, and then pass
# this result as the language input for CMU Sphinx? (lang_detect enrichment)