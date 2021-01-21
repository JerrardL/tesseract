from flask import Flask, request, jsonify
from langdetect import detect

app = Flask(__name__)

@app.route('/', methods=['POST'])
def langauge():
    extraction = request.get_json()
    text_extraction = extraction["text"]
    detection = detect(text_extraction)
    return jsonify({"text": detection})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2468)