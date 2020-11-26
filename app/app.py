from flask import Flask, request
import json

from enrichments.Meta import Meta
from enrichments.DeepSpeech import DeepSpeech
from enrichments.NLP import NLP
from enrichments.OCR import OCR
from enrichments.Captioning import Captioning

app = Flask(__name__)
app.secret_key = 'S3cR3t'
config = None


# Function to format the response
def process_enrichments(data):

    # Init classes
    meta = Meta(config)
    deep_speech = DeepSpeech(config)
    ocr = OCR(config)
    nlp = NLP(config)
    captioning = Captioning(config)

    # Send file through to Tika for metadata
    meta_response = meta.execute(data)

    # Create JSON structure
    formatted_response = {
        "meta": meta_response,
        "extractions": []
    }

    # Check Content-Type of file
    content_type = meta_response["Content-Type"]
    # Attempt to get speech recognition if audio file via DeepSpeech
    if content_type in deep_speech.supported_types:
        response = deep_speech.execute(data)
        formatted_response["extractions"].append({"speech_extraction": response})
    # If not audio file, attempt to perform ocr text extraction via Tika
    else:
        response = ocr.execute(data)
        formatted_response["extractions"].append({"ocr_extraction": response})
    # If text was extracted from the file, attempt to perform nlp via Scapy
    if response:
        nlp_response = nlp.execute(response)
        if nlp_response:
            formatted_response["extractions"].append({"nlp_extraction": nlp_response})
    # If the file was an image, attempt to perform image captioning via Tensorflow
    if content_type in captioning.supported_types:
        captioning_response = captioning.execute(data)
        formatted_response["extractions"].append({"image_captioning": captioning_response})


    # Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)

    return formatted_response_json


# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def upload_binary_file():
    file_as_binary = request.get_data()
    return process_enrichments(file_as_binary)


# Run server, Define config values
if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config = json.loads(config_file.read().decode())

    app.run(host=config["bind_host"], debug=True)
