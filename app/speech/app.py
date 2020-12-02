import json
from os import getenv

from flask import Flask, request, jsonify

from .engine import SpeechToTextEngine


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
