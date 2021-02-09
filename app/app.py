import json
# Import Enrichments
from enrichments.Captioning import Captioning
from enrichments.ImageAICategorisation import ImageAICategorisation
from enrichments.ImageAIClassification import ImageAIClassification
from enrichments.KerasCategorisation import KerasCategorisation
from enrichments.KerasClassification import KerasClassification
from enrichments.Language import Language
from enrichments.Meta import Meta
from enrichments.NLP import NLP
from enrichments.NSFWImageClassifier import NSFWImageClassifier
from enrichments.NSFWImageDetector import NSFWImageDetector
from enrichments.NSFWVideoClassifier import NSFWVideoClassifier
from enrichments.NSFWVideoDetector import NSFWVideoDetector
from enrichments.OCR import OCR
from enrichments.Speech import Speech
from enrichments.TextSentimentAnalysis import TextSentimentAnalysis
from enrichments.Video import Video
from enrichments.VideoOR import VideoOR

from flask import Flask, request

app = Flask(__name__)
app.secret_key = 'S3cR3t'
config = None
ocr_errmsg = "NO OCR EXTRACTION FOUND"

# Main function to format the response
def process_enrichments(data):

    # Init classes
    captioning = Captioning(config)
    imageai_categorisation = ImageAICategorisation(config)
    imageai_classification = ImageAIClassification(config)    
    keras_categorisation = KerasCategorisation(config)
    keras_classification = KerasClassification(config)
    meta = Meta(config)
    nlp = NLP(config)
    nsfw_image_classifier = NSFWImageClassifier(config)
    nsfw_image_detector = NSFWImageDetector(config)
    nsfw_video_classifier = NSFWVideoClassifier(config)
    nsfw_video_detector = NSFWVideoDetector(config)    
    ocr = OCR(config)
    speech = Speech(config)
    text_sentiment_analysis = TextSentimentAnalysis(config)    
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

    def video_files(data):
        # Classify if the video is NSFW
        nsfw_classifier_response = nsfw_video_classifier.execute(data)
        formatted_response["extractions"].append(
            {"nsfw_classification": nsfw_classifier_response})
        # Detect the NSFW content if video has been classified to be at least 50% unsafe
        if nsfw_classifier_response["prediction"]["unsafe average"] > 0.5:     
            nsfw_detector_response = nsfw_video_detector.execute(data)
            formatted_response["extractions"].append(
                {"nsfw_detection": nsfw_detector_response})
        # Perform standard object recognition
        video_or_extraction = video_object_recognition.execute(data)
        formatted_response["extractions"].append({"video_object_recognition": video_or_extraction})
        # Categorise the objects detected
        if video_or_extraction:
            category_response = imageai_categorisation.execute(video_or_extraction['Object Frequency'])
            formatted_response["extractions"].append(
                {"categories": category_response})
        # Convert the video to audio for speech extraction
        video_extraction = video.execute(data)
        formatted_response["extractions"].append(
            {"video_extraction": video_extraction})
        # Perform sentiment analysis on the extracted text
        if video_extraction["extraction"]:
            text_sentiment_response = text_sentiment_analysis.execute(video_extraction["extraction"])
            formatted_response["extractions"].append(
                {"text_sentiment_analysis": text_sentiment_response})
            # Perform NLP on the extracted text
            nlp_response = nlp.execute(video_extraction["extraction"])
            formatted_response["extractions"].append(
                {"nlp_extraction": nlp_response})

    def audio_files(data):
        # Perform speech recognition
        response = speech.execute(data)
        formatted_response["extractions"].append(
            {"speech_extraction": response})
        # Perform sentiment analysis on the extracted text
        if response["extraction"]:
            text_sentiment_response = text_sentiment_analysis.execute(response["extraction"])
            formatted_response["extractions"].append({"text_sentiment_analysis": text_sentiment_response})
            # Perform NLP on the extracted text
            nlp_response = nlp.execute(response["extraction"])
            formatted_response["extractions"].append(
                {"nlp_extraction": nlp_response})

    def image_text_files(data):
        # Attempt OCR extraction on the file
        response = ocr.execute(data)
        formatted_response["extractions"].append(response)
        # If OCR response was blank or whitespace do not perform NLP - NON TEXT IMAGES
        if response["ocr_extraction"] == ocr_errmsg:
            # Classify if the video is NSFW
            if content_type in nsfw_image_classifier.supported_types:
                nsfw_classifier_response = nsfw_image_classifier.execute(data)
                formatted_response["extractions"].append(
                    {"nsfw_classification": nsfw_classifier_response})
                # Detect the NSFW content if video has been classified to be at least 50% unsafe
                if nsfw_classifier_response["prediction"]["unsafe"] > 0.5:     
                    nsfw_detector_response = nsfw_image_detector.execute(data)
                    formatted_response["extractions"].append(
                        {"nsfw_detection": nsfw_detector_response})
                # Attempt to perform image captioning via Tensorflow
                captioning_response = captioning.execute(data)
                formatted_response["extractions"].append(
                    {"image_captioning": captioning_response})
                # Image AI
                # Attempt to classify the image via ImageAI
                imageai_classification_response = imageai_classification.execute(data)
                formatted_response["extractions"].append(
                    {"ImageAI classification": imageai_classification_response})
                # If the image cannot be classified or encounters and error, do not perform categorisation
                if imageai_classification_response and "Error" not in imageai_classification_response:
                    # If objects were detected, attempt to categorise the three most populous objects via gloVe and ImageAI
                    category_response = imageai_categorisation.execute(
                        imageai_classification_response['Object Found, Percentage Probability'])
                    formatted_response["extractions"].append(
                        {"ImageAI categories": category_response})
                # Keras
                # Attempt to classify image via Keras
                keras_classification_response = keras_classification.execute(data)
                formatted_response["extractions"].append(
                    {"Keras classification": keras_classification_response})
                # If the image cannot be classified or encounters and error, do not perform categorisation
                if keras_classification_response and "Error" not in keras_classification_response:
                    # If objects were detected, attempt to categorise the three most populous objects via gloVe and Keras
                        category_response = keras_categorisation.execute(
                            keras_classification_response)
                        formatted_response["extractions"].append(
                            {"Keras categories": category_response})
        elif response["ocr_extraction"]:
            # Perform sentiment analysis on the extracted text
            text_sentiment_response = text_sentiment_analysis.execute(response["ocr_extraction"])
            formatted_response["extractions"].append({"text_sentiment_analysis": text_sentiment_response})
            # Perform NLP on the extracted text
            nlp_response = nlp.execute(response["ocr_extraction"])
            formatted_response["extractions"].append(
                {"nlp_extraction": nlp_response})

    # If the file type is video
    if content_type in video.supported_types:
        video_files(data)
    # If the file type is audio
    elif content_type in speech.supported_types:
        audio_files(data)
    else:
        image_text_files(data)

    # Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)
    json_object = json.loads(formatted_response_json)

    return json_object

# Function for langauge detection via /lang endpoint
def language_detection(data):

    # Init classes
    meta = Meta(config)
    speech = Speech(config)
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
    if content_type in speech.supported_types:
        response = speech.execute(data)
        formatted_response["extractions"].append(
            {"speech_extraction": response})
        # Attempt to detect language of speech here via langdetect:
        language = language.execute(response["extraction"])
        formatted_response["extractions"].append(
            {"language_detected": language})
    # If not audio file, attempt to perform ocr text extraction via Tika
    else:
        response = ocr.execute(data)
        formatted_response["extractions"].append(response)
        # Attempt to detect language of text here via langdetect:
        language = language.execute(response["ocr_extraction"])
        formatted_response["extractions"].append(
            {"language_detected": language})
    # TODO Attempt to translate text if not english
    formatted_response["extractions"].append(
        {"translation": "TO BE CONFIGURED"})

    # Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)
    json_object = json.loads(formatted_response_json)

    return json_object

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
