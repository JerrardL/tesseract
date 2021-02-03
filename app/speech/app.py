from flask import Flask, request, jsonify
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment

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



# new-speech - intended to replace Speech enrichment.
# Works well and seemingly faster than DeepSpeech.
# Uses CMU Sphinx which includes models for other languages.
# Issue is than language must be specified first before CMU Sphinx
# uses that model to transcribe the audio.
# Is there any way to detect a langauge from audio, and then pass
# this result as the language input for CMU Sphinx? (lang_detect enrichment)