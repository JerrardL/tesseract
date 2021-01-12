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
from enrichments.Language import Language
from enrichments.Video import Video
from enrichments.VideoOR import VideoOR

app = Flask(__name__)
app.secret_key = 'S3cR3t'
config = None
ocr_errmsg = "NO OCR EXTRACTION FOUND"

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
    video = Video(config)
    video_object_recognition = VideoOR(config)

    # METADATA
    # Send file through to Tika for metadata
    meta_response = meta.execute(data)

    # Create JSON structure
    formatted_response = {
        "meta": meta_response,
        "extractions": []
    }

    # Check Content-Type of file
    content_type = meta_response["Content-Type"]

    # VIDEO FILES
        # VIDEO OBJECT RECOGNITION
        # If VIDEO FILE, first attempt to perform object recogntion via imageAI
    if content_type in video.supported_types:
        video_or_extraction = video_object_recognition.execute(data)
        formatted_response["extractions"].append({"video_object_recognition": video_or_extraction})
        # VIDEO CATEGORISATION
            # If objects were detected, attempt to categorise the three most populous objects via gloVe

        # SPEECH RECOGNITION for VIDEO
            # Then attempt to convert video file to audio for extraction, via pydub
            # Then attempt to do speech recognition on the new audio file via DeepSpeech
        video_extraction = video.execute(data)
        formatted_response["extractions"].append({"video_extraction": video_extraction})
        if video_extraction["extraction"]:
            # NLP
            # If text was extracted from the file, attempt to perform nlp via Scapy
            nlp_response = nlp.execute(video_extraction["extraction"])
            formatted_response["extractions"].append({"nlp_extraction": nlp_response})
    # AUDIO FILES
        # SPEECH RECOGNITION
            # If AUDIO FILE, attempt to get speech recognition if audio file via DeepSpeech
    elif content_type in speech_recognition.supported_types:
        response = speech_recognition.execute(data)
        formatted_response["extractions"].append({"speech_extraction": response})
        if response["extraction"]:
            # NLP
                # If text was extracted from the file, attempt to perform nlp via Scapy
            nlp_response = nlp.execute(response["extraction"])
            formatted_response["extractions"].append({"nlp_extraction": nlp_response})
    # If NOT AUDIO OR VIDEO FILE, attempt to perform ocr text extraction via Tika
    else:
        response = ocr.execute(data)
        formatted_response["extractions"].append(response)
        # If OCR response was blank or whitespace do not perform NLP
        if response["ocr_extraction"] == ocr_errmsg:
            # IMAGE CAPTIONING
                # If the file was an image, attempt to perform image captioning via Tensorflow
            if content_type in captioning.supported_types:
                captioning_response = captioning.execute(data)
                formatted_response["extractions"].append({"image_captioning": captioning_response})
                # IMAGE CLASSIFICATION
                    # Attempt to classify the image via keras
                classification_response = classification.execute(data)
                formatted_response["extractions"].append({"classification": classification_response})
                # If the image cannot be classified or encounters and error, do not perform categorisation
                if "Error" not in classification_response:
                    # IMAGE CATEGORISATION    
                        # If a classification was extracted, attempt to categorise the prediction via gloVe
                    if classification_response:
                        category_response = categorisation.execute(classification_response)
                        formatted_response["extractions"].append({"categories": category_response})
        elif response["ocr_extraction"]:
            # NLP
                # If text was extracted from the file, attempt to perform nlp via Scapy
            nlp_response = nlp.execute(response["ocr_extraction"])
            formatted_response["extractions"].append({"nlp_extraction": nlp_response})

    # Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)

    return formatted_response_json

def language_detection(data):
    
    # Init classes
    meta = Meta(config)
    speech_recognition = Speech(config)
    ocr = OCR(config)
    language = Language(config)

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
        # Attempt to detect language of speech here via langdetect:
        language = language.execute(response["extraction"])
        formatted_response["extractions"].append({"language_detected": language})
    # If not audio file, attempt to perform ocr text extraction via Tika
    else:
        response = ocr.execute(data)
        formatted_response["extractions"].append(response)
        # Attempt to detect language of text here via langdetect:
        language = language.execute(response["ocr_extraction"])
        formatted_response["extractions"].append({"language_detected": language})
    # TODO Attempt to translate text if not english
    formatted_response["extractions"].append({"translation": "TO BE CONFIGURED"})
  
    # Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)

    return formatted_response_json

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def upload_binary_file():
    file_as_binary = request.get_data()
    return process_enrichments(file_as_binary)

# Language Route:
# Use POST method with binary and file to upload via Postman
@app.route('/lang', methods=['POST'])
def upload_binary_language_file():
    file_as_binary = request.get_data()
    return language_detection(file_as_binary)

# Run server, Define config values
if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config = json.loads(config_file.read().decode())

    app.run(host=config["bind_host"], debug=True)
