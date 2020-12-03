from flask import Flask, request
import json
# Import enrichments
from enrichments.Meta import Meta
from enrichments.Speech import Speech
from enrichments.NLP import NLP
from enrichments.OCR import OCR
from enrichments.Captioning import Captioning
from enrichments.Classification import Classification
from enrichments.Categorisation import Categorisation

app = Flask(__name__)
app.secret_key = 'S3cR3t'
config = None

# Function to format the response
def process_enrichments(data):

    # Init classes
    meta = Meta(config)
    speech_recognition = Speech(config)
    ocr = OCR(config)
    nlp = NLP(config)
    captioning = Captioning(config)
    classification = Classification(config)
    categorisation = Categorisation(config)

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
    if content_type in speech_recognition.supported_types:
        response = speech_recognition.execute(data)
        formatted_response["extractions"].append({"speech_extraction": response})
    # If not audio file, attempt to perform ocr text extraction via Tika
    else:
        response = ocr.execute(data)
        formatted_response["extractions"].append(response)
    # If text was extracted from the file, attempt to perform nlp via Scapy
    if response:
        nlp_response = nlp.execute(response)
        if nlp_response:
            formatted_response["extractions"].append({"nlp_extraction": nlp_response})
    # If the file was an image, attempt to perform image captioning via Tensorflow
    if content_type in captioning.supported_types:
        captioning_response = captioning.execute(data)
        formatted_response["extractions"].append({"image_captioning": captioning_response})
        # Attempt to classify the image via keras
        classification_response = classification.execute(data)
        formatted_response["extractions"].append({"classification": classification_response})
        # If a classification was extracted, attempt to categorise the prediction via gloVe
        if classification_response:
            category_response = categorisation.execute(classification_response)
            formatted_response["extractions"].append({"categories": category_response})

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
