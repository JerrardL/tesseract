import requests
from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import json

# Init App
app = Flask(__name__)
app.secret_key = 'S3cR3t'
# Upload folder destination & set allowed extensions
upload_folder = './uploaded'
allowed_extensions = None
app.config['upload_folder'] = upload_folder

#Check file extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

#Function to format the response
def format_response(file):
    headers = {'Accept': 'application/json'}
    nlp_headers = {'Content-Type': 'application/json'}
    # Send file through to Tika for metadata
    resp_meta = requests.put(meta_endpoint, data=file, headers=headers)
    meta = resp_meta.json()
    # Create JSON structure
    formatted_response = {
        "meta": meta,
        "extractions": []
    }
    # Check Content-Type of file
    # Attempt to get speech recognition if audio file via DeepSpeech
    if meta["Content-Type"] in speech:
        speech_response = requests.post(speech_endpoint, data=file)
        extraction = speech_response.json()["text"]
        formatted_response["extractions"].append({"speech_extraction": extraction})
    # If not audio file, attempt to perform ocr text extraction via Tika
    else:
        ocr_response = requests.put(ocr_endpoint, data=file)
        extraction = ocr_response.text.replace('\n', ' ')
        formatted_response["extractions"].append({"ocr_extraction": extraction})
   # If text was extracted from the file, attempt to perform nlp via Scapy 
    if extraction:
        nlp_data = {'text': extraction, 'model': 'en'}
        nlp_response = requests.post(nlp_endoint, data=json.dumps(nlp_data), headers=nlp_headers)
        nlp_extraction = nlp_response.json()
        if nlp_extraction:
            formatted_response["extractions"].append({"nlp_extraction": nlp_extraction})

    #Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)

    return formatted_response_json

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def upload_binary_file():
    file_as_binary = request.get_data()
    return format_response(file_as_binary)

# Run server, Define config values
if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config = json.loads(config_file.read().decode())
        allowed_extensions = config["allowed_extensions"]
        meta_endpoint = config["meta_endpoint"]
        ocr_endpoint = config["ocr_endpoint"]
        nlp_endoint = config["nlp_endpoint"]
        speech_endpoint = config["speech_endpoint"]
        speech = config["enrichments"]["speech_recognition"]
        host_zero = config["host_zero"]

# Optional Route?:
# Use GET method to make request via web browser UI
# Use POST method with form-data and file to upload, named 'file' via Postman
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user doesn't select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             return format_response(file)
#     return render_template('index.html')

    app.run(host=host_zero, debug=True)