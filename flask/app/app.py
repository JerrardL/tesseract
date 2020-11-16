import os
import requests
# Import Flask
from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json
# Init App
app = Flask(__name__)
#Upload folder destination & set allowed extensions
upload_folder = './uploaded'
allowed_ext = {'pdf','png','gif','jpeg','jpg','txt'}

app.config['upload_folder'] = upload_folder
# Create memory location for metadata
memory = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext
# Main Route:
# Use GET method to make request via web browser
# Use POST method with form-data and file to upload, named 'file' via Postman
# Will redirect through all endpoints, starting with /uploads/<filename>
@app.route('/', methods=['GET','POST'])
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_folder'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')
# Secondary Route:
# Use POST method with binary and file to upload via Postman
# Will redirect to /result/<filename> endpoint
# Must add methods=['POST'] to use directly. Will disable POST methods in other endpoints 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file = open('./uploaded/%s' % filename, 'rb')
    headers = {'Accept':'application/json'}
    resp_meta = requests.put("http://tika:9998/meta", data=file, headers=headers)
    meta = resp_meta.json()
    memory.append(meta)

    return redirect(url_for('result', filename=filename))
# cdd Route:
# Use POST method with binary and file to upload via Postman
# Will redirect to /result/<filename> endpoint
# Must add methods=['POST'] to use directly. Will disable POST methods in other endpoints 
@app.route('/new/<filename>', methods=['POST'])
def upload_new_file(filename):
    file = open('./uploaded/%s' % filename, 'rb')
    headers = {'Accept':'application/json'}
    resp_meta = requests.put("http://tika:9998/meta", data=file, headers=headers)
    meta = resp_meta.json()
    memory.append(meta)

    return redirect(url_for('result', filename=filename))
# Indirect Route:
# To be accessed as a redirect from /uploads/<filename> route
# Sending a direct POST request to this endpoint will emit metadata
# Must add methods=['POST'] to use directly. Will disable POST methods in other endpoints 
@app.route('/result/<filename>')
def result(filename):
    file = open('./uploaded/%s' % filename, 'rb')
    resp_extraction = requests.put("http://tika:9998/tika", data=file)
    extracted = resp_extraction.text
    extraction = extracted.replace('\n',' ')

    #Create JSON structure
    formatted_response = {
        "meta": memory[0],
        "extractions": extraction
    }
    formatted_response_json = json.dumps(formatted_response, indent=4)
    memory.clear()

    return formatted_response_json

# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)