# File Information Extractor
An application that can provide various different extractions from a file type based on a variety of different enrichments.
A file is uploaded via binary to an endpoint, and a JSON response is returned. Based on the file type, the JSON response will 
return different output. Below will be a summary of the different enrichments created so far, and the corresponding supported file types
for which they will provide output, along with how to download the required models where necessary. You can read through each enrichment, or jump to the TL;DR section from the contents for quick text on installation and how to download the models.
## Contents
- [Meta](#meta)
- [Optical Character Recognition (OCR)](#optical-character-recognition-ocr)
- [Natural Language Processing (NLP)](#natural-language-processing-nlp)
- [Image Captioning](#image-captioning)
- [Model Setup](#model-setup)
- [Image Classification](#image-classification)
- [Video Object Recognition](#video-object-recognition)
- [Categorisation](#categorisation)
- [Speech Recognition](#speech-recognition)
- [Text Sentiment Analysis](#text-sentiment-analysis)
- [TL;DR (Running The App)](#tldr-running-the-app)
- [In Production](#in-production)

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
This enrichment provides image captioning for image files. This is done using a docker image, and corresponding python script files which work with the image. The docker image is an Image Caption Generator, provided by Codait, as part of an IBM Developer Code Model Asset Exchange. The docker hub link can be found [here](https://hub.docker.com/r/codait/max-image-caption-generator). Captioning works using Tensorflow framework, and different ML computer vision models, which have been trained using the [COCO Dataset](https://cocodataset.org/#home). Supported types for Image Captioning include:
```
image/png,
image/jpg,
image/jpeg,
image/gif
```
This enrichment uses models which require some data to be pre downloaded before use. Models need to be set up in a particular way in order for them to work with their enrichments. You will need to create a separate `models` directory, which will then act as a hub for models for all other enrichments. **The models that are used for enrichments are usually quite large files, and are therefore not included in this repository. Links will be provided for each enrichment on where to download the models from where necessary.**

#### Model Setup
1. Create a separate `models` folder just **outside** of this repository. The structure should be similar to this:
```
/models
/tesseract
```
2. Within the models folder, create a subdirectory called `captioning`. This is relative to this specific enrichment.
3. Within that subdirectory, create another named `assets`.
4. In this directory, you'll need to place certain files. The files can be sourced [here](https://github.com/IBM/MAX-Image-Caption-Generator/blob/master/assets). First download the `word_counts.txt` file either from downloading the repo and navigating to the file, or another method. Place this file in this subdirectory. 
5. From the same page, you'll also need to download the `assets.tar.gz` file, which is accessed by clicking the *IBM Cloud Object Storage* link. Once downloaded, unzip the file and you should see a `checkpoint` folder.
5. Copy the **whole** folder with its contents into the `assets` folder.
6. Your folder structure should be `models/captioning/assets` which should include the `word_counts.txt` file, and another folder `checkpoint`, which should include four additional files.

Once the models have been downloaded and the folder structure has been created, the enrichment will work, allowing access offline also. **Image Captioning will only work on image files that do not include text.** This ensures only images with objects or things that can actually be captioned are sent through to the caption generator. Images that include text and other objects will not go through image captioning. Below is an extract example of the Image Captioning output:
```
"image_captioning": {
    "predictions": [
        {
            "caption": "a group of people standing next to each other .",
            "index": "0",
            "probability": 0.0029328946598735964
        },
...
```
`"caption"` refers to the caption the generator has provided for the image file, `"index"` refers to the caption number. The generator will provide 3 different captions, ordered by their `"probability"`.

### ***
***The remaining enrichments do not use docker images, and are all created from python scripts which use various different libraries and model data to function. All libraries and Python versions required for each enrichment to work are specified in the enrichments corresponding requirements file and Dockerfile, which will install the libraries needed. Certain enrichments, such as Speech Recognition, require the models to be set up in a certain way from within the `models/` directory in order for them to be read correctly. Instructions will also be provided on how to set up these folders. Ensure that you have followed the first step in the [Model Setup](#model-setup) so that you have already got a base model structure before continuing.***
### ***

### Image Classification
This enrichment provides classification on image files that have already gone through image captioning. Classification attempts to detect and name the objects found within an image. This is done from a variety of python script files which use different libraries depending on the framework being used. Images will go through two sets of classification.
- **Keras Classification**, where images will be classified using the Keras framework and VGG16 computer vision model, trained with data from [ImageNet](http://www.image-net.org/).
- **ImageAI Classification**, where images will be classified using the ImageAI framework, which uses a [YoloV3](https://pjreddie.com/darknet/yolo/) model for detection, trained with its own data.
The reasoning for using two classification models is that the ImageAI classifier has the ability to detect people, whereas the Keras classifier can detect more specific objects, such as a weapon, or clothing. Classification immediately follows [Image Captioning](#image-captioning), and so they have the same supported file types.
#### Classification Models
You will need to have the training models pre downloaded in order for this enrichment to work:
1. From your `models/` folder, create a new folder named `classification`.
2. Within this folder, create another sub folder named `keras`.
3. Within this folder, create a final sub folder named `models`. You'll need to place the keras classification models here; the [ImageNet JSON](https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json), and the [VGG16 Weights](https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels.h5). **DO NOT rename these files.**
4. Your folder structure here should be `models/classification/keras/models` which should include the two files from the previous step.
5. From your `models/` folder, create a new folder named `object_recognition`. The ImageAI classification model will go here, as it can also be used for detect objects in video files [also](#video-object-recognition).
6. Download the [YoloV3](https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5) model file. Leave the file name unchanged.

Once the models have been downloaded and the folder structure has been created, the enrichment will work, allowing access offline also. Similar to Image Captioning, **Image Classification will only work on image files that do not contain text**. As it follows on from image captioning, it has the same idea that only images with objects in them can be classified. Below is an extract example of the Image Classification output:
```
"ImageAI classification": {
    "Object Found, Percentage Probability": [
        [
            "person",
            99
...
{
    "Keras classification": {
        "Best Prediction": {
            "Confidence": "0.18676902",
            "Prediction": "maillot"
        },
...
```
ImageAI classification includes the object found, along with the percentage probability for that object. Keras classification includes 3 different predictions, based on confidence levels.

### Video Object Recognition
This enrichment attempts to name and detect objects within a video file. It works in a similar way to [Image Classification](#image-classification) for ImageAI. The only real difference is the detector is detecting video and not an image file. Esentially the video function looks at every frame, and treats each frame as an image, looking for objects to detect. It will produce an object frequency, showing how many times it detected an object. This **is not** in correlation to how many objects of that type are in the video. As the function goes through each frame individually, it counts the objects detected in each frame, and provides a tallied result. Object Frequency can be seen as a good way to see what objects are most prominent in a video. Supported types for Video Object Recognition include:
```
video/mpeg,
video/wemb,
video/mp4
```

Provided you downloaded the models for [image classification](#image-classification), you should already have the required model for video object recognition, located in your `models/object_recognition` folder.

**Video Object Recognition only works on video files**, which is self explanatory. Below is an extract example of the Video Object Recognition output:
```
"video_object_recognition": {
    "Object Frequency": [
        [
            "car",
            409
        ],
        [
            "bus",
            114
        ],
        [
            "person",
            103
        ],
...
```
Remember that Object Frequency relates to how many times the detector has detected that object, per frame, as a total of all frames combined, not how many of that object was detected in the video.

### Categorisation
This enrichment provides categorisation on image and video files which have already been classified. This works by using the classified results from image classification or video object recognition to categorise them into departments which share similarities. This works using a gloVe text file which contains a vast amount of words which have been placed into pre defined categories. gloVe represents [Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/); a learning algorithm created by people at Stanford University. Categorisation is dependant on classification. It will not work if an image or video has not been classified. Therefore it shares the same supported file types respectively.

Currently, 8 predefined categories have been made for categorisation as follows:
```
"Violent": ["rifle", "handgun", "firearm", "blade", "knife", "blood"],
"Location": ["beach", "park", "forest", "river", "garden", "mountain"],
"Dogs": ["poodle", "labrador", "great dane", "chihuahua", "pug", "bulldog", "dog"],
"Vehicle": ["car", "van", "truck", "hatchback", "bus", "lorry"],
"People": ["man", "woman", "child", "baby", "girl", "boy", "person"],
"Clothing": ["jacket", "shorts", "skirt", "trousers", "hat", "shirt"],
"Activities": ["swimming", "running", "walking", "cycling", "jogging", "golfing"],
"Animals": ["giraffe", "zebra", "lion", "monkey", "bird", "cat"]
```
Words that have been classified, will be checked against the gloVe file for similar words. They will then be compared to these categories. If a word is found to be most similar to the other words in that category, it will be categorised as the corresponding topic. Categorisation can help to define an overall depiction of what material is contained in an image.
#### Categorisation Models
Categorisation requires a model to be pre downloaded to work:
1. From your `models/` folder, create a new folder named `categorisation`.
2. Within this folder, download this [gloVe file](http://nlp.stanford.edu/data/glove.6B.zip). Unzip the file, and move the `glove.6B.300d.txt` file into your `models/categorisation` location. Do not rename the file.

Once the models have been downloaded and the folder structure has been created, the enrichment will work, allowing access offline also. **Categorisation only works on image or video files that have already been classified.** As catgorisation is dependant on the classification results, it will not work if an image or video has not produced any classification results. If no objects have been detected, the file cannot be categorised. As Image Classification uses 2 different frameworks - ImageAI and Keras - categorisation provides separate results for these two classifiers. Video categorisation will appear under ImageAI categorisation, as it uses the same detector and model as ImageAI classification. Below is an extract example of the Categorisation output:
```
"ImageAI categories": {
    "Best Prediction Category": "People",
    "time_taken": 0.06624126434326172
}
},
...
"Keras categories": {
    "Best Prediction Category": "Clothing",
    "Low Prediction Category": "Clothing",
    "Mid Prediction Category": "Clothing",
    "time_taken": 0.05859875679016113
}
...
```

### Speech Recognition
This enrichment provides speech recognition by transcribing spoken audio detected in both audio and video files into text. This is done from a python script which uses the SpeechRecognition (SR) library. Supported types for Speech Recognition include:
```diff
audio/aac,
audio/vnd.wave,
audio/mpeg,
+audio/wav,
audi/webm,
+video/mpeg,
+video/wemb,
+video/mp4
```
***This enrichment uses various different models which must be downloaded and then follow a strict folder and file naming pattern. This results in the setup being a potentially confusing and convoluted process. Ensure to follow the steps correctly.***

The SR library contains support for many different speech libraries but this enrichment uses the CMU Sphinx library, mainly as it can be used offline. Currently, this library only accepts audio files that are in `audio/wav'` format. Video files are always converted to .wav format for audio, before the audio file is then sent through speech recognition. For now, we will be using the SpeechRecognition library with CMU Sphinx, as it allows support for multiple languages. This code is locaded in the 'newspeech' folder. 


#### Speech Recognition Models
In order for this to work, the data must be predownloaded for PocketSphinx to use. These models can be downloaded from an open source third-party website, SourceForge. The models can be found [here](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/).

The default model used by the recogniser is EN-US, so ensure you download the *US English* model first (cmusphinx-en-us-8khz-5.2.tar.gz). The tar file will need to be unzipped first, and will include various different files that will need to be renamed and restructured.
1. From your `models/` folder, create a new folder named `categorisation`.

### Text Sentiment Analysis
This enrichment provides sentiment analysis on text that has been extracted from image, video, or audio files. This uses the VADER library, within the [NLTK](https://www.nltk.org/) library to provide sentiment analysis on any text that has been extracted. The sentiment result will show how strong it things the text can be perceived as positive, negative or neutral. There is also a compound response which uses a different measurement. It is a summation of valence scores of each word in the lexicon, normalised to values between -1 being most extreme negative, and 1 being most extreme positive. The idea is that you can have have an overall positive sentiment, which may contain stronger classed negative words, but not enough to change the overall text sentiment. Supported types for text sentiment analysis include:
```
image/png,
image/jpg,
image/jpeg,
image/gif,
application/pdf,
audio/aac,
audio/vnd.wave,
audio/mpeg,
audio/wav,
audi/webm,
video/mpeg,
video/wemb,
video/mp4
```

#### Sentiment Analysis Models
Text Sentiment Analysis requires a model to be pre downloaded to work:
1. From your `models/` folder, create a new folder named `sentiment`.
2. Start an interactive python shell, using your command line, terminal or any other method.
3. Run the following:
```
import nltk
nltk.download('vader_lexicon')
```
4. Once this has been downloaded. Navigative to to your `C:\Users\AppData` location, dependant on your environment. If AppData is not showing from users you may have to check that hidden files are being shown.
5. From here navigate to `\Roaming\nltk_data\sentiment\vader_lexicon\vader_lexicon`
6. Here you will see the `vader_lexicon.txt` file - copy this file to your `models/sentiment` location.


Once the models have been downloaded and the folder structure has been created, the enrichment will work, allowing access offline also. **Text Sentiment Analysis only works with files that have extrated a text output.** This varies depending on file type, however, if there is no ocr extraction, or text extraction from audio or video via speech recognition, then there will be no text that can be analysed via sentiment analysis. Below is an extract example of the text sentiment analysis output:
```
"text_sentiment_analysis": {
    "sentiment_analysis": {
        "compound": -0.1531,
        "negative": 0.097,
        "neutral": 0.833,
        "positive": 0.069
    },
...
```

### TL;DR (Running The App)
The application is written mainly in python, but runs using various containers within Docker, composed from a single Docker Compose file. Each enrichment is either made from an initial python script that uses Flask as a web framework for sending requests, or from a pre created Docker image from Docker Hub. During testing, requests are made via Postman.
**You will need both Docker and the enrichment models/datasets pre downloaded as a prerequisite to run the application.**
1. Ensure you have Docker installed. You can download it [here](https://www.docker.com/products/docker-desktop).
2. If you did not read through the enrichments, you need to make sure you have downloaded the appropriate models and datasets, and have set up your model structure accordingly. If you did, you can skip this step.
    - Follow the [model setup](#model-setup) to create your model directory, and download the models for captioning.
    - Download and place the other models and datasets for [classification](#classification-models), [categorisation](#categorisation-models), [text sentiment analysis](#sentiment-analysis-models), and [speech-recognition](#speech-recognition-models).
3. Run `docker-compose build` from your terminal to build the application. Ensure you are at the root folder location that contains the `docker-compose.yml` file before running the command (/tesseract).
4. Once the containers have been built, run `docker-compose up` to start the containers. You will see text output for each container as they start up. Give it a minute to fully load the containers. Usually video object recognition is last to start up, and you should see `Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)` when it is ready.
5. You can now send a binary file via a POST request using postman or any other service to `http://localhost:5001/` where `localhost` is the host number of your machine. The running terminal will show progress output and any potential errors.

### In Production
The following is currently in production and has not yet been added to this offine application version. Once they have been configured and tested the README will be updated to reflect this:
- New NSFW enrichment that can detect if material is safe or explicit (nsfw_classifier & nsfw_detector).
- Adding support to detect what language is being spoken directly from audio for the speech recognition enrichment.
- Adding support for different audio types other than .wav to be accepted by the speech recognition enrichment.
- New enrichment to translate text into different languages.
