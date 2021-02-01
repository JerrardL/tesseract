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
The metadata provided will be slightly different for each file type, but they will all contain generic information such as file name and when it was created. Below is an extract of what the Meta output will look like:
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
"image/png",
"image/jpg",
"image/jpeg",
"image/gif",
"application/pdf"
```
Below is an extract of what the OCR output will look like:
```
"ocr_extraction": "The quick brown fox jumped over the lazy dog.",
"time_taken": 0.257
```

- Speech Recognition where audio and video files are transcribed into text (via. DeepSpeech & CMU Sphinx)
- Optical Character Recognition (OCR) Extraction where text found in non-audio files such as images or documents is extracted (via. Tika)
- Natural Language Processing (NLP) on text extracted files (via. spaCy)
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
