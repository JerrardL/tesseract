# File Information Extractor
A project that provides various different extractions from a file based on a variety of different enrichments.
A file is uploaded via binary, and a json response is returned, containing:
- File Metadata (via. Tika)
- Speech Recognition where audio and video files are transcribed into text (via. DeepSpeech & CMU Sphinx)
- Optical Character Recognition (OCR) Extraction where text found in non-audio files such as images or documents is extracted (via. Tika)
- Natural Language Processing (NLP) on text extracted files (via. spaCy)
- Image Captioning on image files (via. Tensorflow)
- Image Classification on image files. (via. Keras, InceptionResNetV2 Model & ImageAI)
- Catergorisation on image files that have gone through image classification (via. gloVe)
- Video Object Recognition (via. ImageAI)
- Categorisation on video files that have gone through video object recognition (via. gloVe)
- Semantic Analysis on text extracted from images, audio or video (via. NLTK)

## Datasets Used include:
- YOLO v3 with ImageAI
- VADER with NLTK
- PocketSphinx & SourceForge with CMU Sphinx
- IBM Cloud Object Storage & MIT with Tensorflow
- gloVe
