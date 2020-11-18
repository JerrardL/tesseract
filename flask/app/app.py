import requests
from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import json

# Init App
app = Flask(__name__)
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
    resp_meta = requests.put(meta_endpoint, data=file, headers=headers)
    meta = resp_meta.json()
    resp_extraction = requests.put(ocr_endpoint, data=file)
    extracted = resp_extraction.text
    extraction = extracted.replace('\n', ' ')
    # Create JSON structure
    formatted_response = {
        "meta": meta,
        "extractions": extraction
    }
    #Format JSON
    formatted_response_json = json.dumps(formatted_response, indent=4)

    return formatted_response_json


# Main Route:
# Use GET method to make request via web browser UI
# Use POST method with form-data and file to upload, named 'file' via Postman
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user doesn't select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return format_response(file)
    return render_template('index.html')

# Secondary Route:
# Use POST method with binary and file to upload via Postman
@app.route('/binary', methods=['POST'])
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
        host_zero = config["host_zero"]
        print(allowed_extensions)

    app.run(host=host_zero, debug=True)