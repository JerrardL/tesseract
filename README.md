# File Information Extractor
An application that can provide various different extractions from a file type based on a variety of different enrichments.
A file is uploaded via binary to an endpoint, and a JSON response is returned. Based on the file type, the JSON response will 
return different output. Below is a summary of the different enrichments created so far, and the corresponding supported file types
for which they will provide output.
## Enrichments
### Meta
This enrichment provides metadata for the provided file. A docker image which uses the Apache Tika framework, is used for this. **Metadata can be extracted from any file type.** Current supported file types for this application include:
```
image/png
image/jpg
image/jpeg
image/gif
application/pdf
text/plain
audio/aac
audio/vnd.wave
audio/mpeg
audio/wav
audi/webm
video/mpeg
video/wemb
video/mp4
```
The metadata provided will be slightly different for each file type, but they will all contain generic information such as file name and when it was created. Below is an extract example of the Meta output:
```
"meta": {
    "Content-Type": "image/jpeg",
    "File Name": "tester_file.jpeg",
    "File Size": "53777 bytes"
...
```
The metatdata will usually appear at the bottom of the overall output. Each enrichment will also include an output for `time_taken` which shows how long it took for the process to return a result.
### Optical Character Recognition (OCR)
This enrichment provides OCR extraction for files that appear to include text. An Apache Tika docker image is also used for this. OCR will simply transcribe any text found into the output. This can be from either an application format such as a pdf, or an image that contains text. Some images that may not appear to include text still may still produce an unhelpful OCR output, but this could be due to if the file has been edited. Supported types for OCR include:
```
image/png,
image/jpg,
image/jpeg,
image/gif,
application/pdf
```
Below is an extract example of the OCR output:
```
"ocr_extraction": "The quick brown fox jumped over the lazy dog.",
"time_taken": 0.257
```
### Natural Language Processing (NLP)
This enrichment provides NLP on files where text has been extracted. NLP works by trying to make sense of the text by placing known words into certain categories it thinks that they are related to. This is done using a docker image, which uses the spaCy API. The docker hub link can be found [here](https://hub.docker.com/r/jgontrum/spacyapi/). The page also includes links to GitHub documentation. 

**NLP will only attempt to provide output if text has been extracted from the file.** If there is no OCR extraction, then NLP will not be perfomed. As NLP will read input directly from the OCR extraction, the only supported type here is `text/plain`. Below is an extract example of the NLP output:
```
"nlp_extraction": [
    {
        "end": 17,
        "start": 6,
        "text": "Jane Doe",
        "type": "PERSON"
...
```
`"end"` refers to the location of the last character, whilst `"start"` refers to the first. `"text"` is the text that was picked up and `"type"` is the category type that spaCy has determined for the text. More information on different types and how spaCy works can be found from the GitHub documentation, located in the link provided above.

### Image Captioning
This enrichment provides image captioning for image files. This is done using a docker image, and corresponding python script files which work with the image. The docker image is an image Caption Generator, provided by Codait, as part of an IBM Developer Code Model Asset Exchange. The docker hub link can be found [here](https://hub.docker.com/r/codait/max-image-caption-generator). Captioning works using Tensorflow framework, and different ML data models, which have been trained using the [COCO Dataset](https://cocodataset.org/#home). Supported types for Image Captioning include:
```
image/png,
image/jpg,
image/jpeg,
image/gif
```
Use of this enrichment requires models to be pre downloaded.

### ***
***The remaining enrichments do not use docker images, and are all created from python scripts which use various different libraries and model data to function. All libraries and Python versions required for each enrichment to work are specified in the enrichments corresponding requirements file and Dockerfile, which will install the libraries needed. The models that are used are usually quite large files, and are therefore not included in this repository. Links will be provided for each enrichment on where to download the models from where necessary. Certain enrichments, such as Speech Recognition, require the models to be set up in a certain way in order for them to be read correctly. Instructions will also be provided on how to set up these model folders.***
### ***

### Speech Recognition
This enrichment provides speech recognition by transcribing spoken audio detected in both audio and video files into text. This is done from a python script which uses the SpeechRecognition (SR) library. Supported types for Speech Recognition include:
```
audio/aac,
audio/vnd.wave,
audio/mpeg,
audio/wav,
audi/webm,
video/mpeg,
video/wemb,
video/mp4
```
***This enrichment makes up two separate folders, one of which uses various different models which must be downloaded and then follow a strict folder pattern. This results in the setup being a potentially confusing and convoluted process. Ensure to follow the steps correctly.***

The SR library contains support for many different speech libraries but this enrichment uses the CMU Sphinx library, mainly as it can be used offline. Currently, this library only accepts audio files that are in `audio/wav'` format. Video files are always converted to .wav format for audio (See Video enrichment). Previously, a different speech recognition service, DeepSpeech, was being used for transcribing which allowed other audio file types. This is not in use for now, but its files are still contained in the 'speech' folder for later potential use. For now, we will be using the SpeechRecognition library with CMU Sphinx, as it allows support for multiple languages. This code is locaded in the 'newspeech' folder. In order for this to work, the data must be predownloaded for PocketSphinx to use. These models can be downloaded from an open source third-party website, SourceForge. The models can be found [here](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/).

The default model used by the recogniser is EN-US, so ensure you download the *US English* model first (cmusphinx-en-us-8khz-5.2.tar.gz). The tar file will need to be unzipped first, and will include various different files that will need to be renamed and restructured.
#### Model Setup
Outside of this repository you will need to create a separate `models` folder. This folder will become populated with these models and other models that will be used by other enrichments



- Image Captioning on image files (via. Tensorflow)
- Image Classification on image files. (via. Keras, InceptionResNetV2 Model & ImageAI)
- Catergorisation on image files that have gone through image classification (via. gloVe)
- Video Object Recognition (via. ImageAI)
- Categorisation on video files that have gone through video object recognition (via. gloVe)
- Semantic Analysis on text extracted from images, audio or video (via. NLTK)

The application is written mainly in python, but runs using various containers within Docker, composed from a single Docker Compose file. Each enrichment is either made from an initial python script that uses Flask as a web framework for sending requests, or from a pre created Docker image from Docker Hub. During testing, requests are made via Postman.

### Prerequisites
You will need both Docker and the used models/datasets as a prerequisite to run the application. The models have not been uploaded due to their size but they can be be found and downloaded from these sites:
#### Datasets/Models used include:
- YOLO v3 with ImageAI
- VADER with NLTK
- PocketSphinx & SourceForge with CMU Sphinx
- IBM Cloud Object Storage & MIT with Tensorflow
- gloVe
- Model for DeepSpeech

Pull the initial tesseract repo to your local computer. Create a new subdirectory, outside of tesseract, named models. Place your saved models in this new directory, with each model in its own subdirectory, name respective to the enrichment it is being used for E.g.:
```
models/captioning/...
models/categorisation/...
models/object_recognition/...
```
### Installation
The set up is very simple. Once you have downloaded the models and created the subdirectory for them and installed Docker, to run the application enter `docker-compose up --build` into your terminal from the root folder location (/tesseract).
Most enrichments have been created from a python script that uses Flask to make requests, with the exception of the Metadata, OCR and NLP enrichments which use the following docker images, made available from Docker Hub:
#### Docker Images used include:
- Apache Tika
- spaCy API
