# File Information Extractor
A project that provides various different extractions from a file based on a variety of different enrichments.
A file is uploaded via binary, and a json response is returned, containing:
- File Metadata (via. Tika)
- Speech Recognition where audio and video files are transcribed into text. (via. DeepSpeech)
- Optical Character Recognition (OCR) Extraction where an text found in non-audio files such as images or documents is extracted. (via. Tika)
- Natural Language Processing (NLP) on text extracted files. (via. spaCy)
- Image Captioning on image files. (via. Tensorflow)
- Image Classification on image files. (via. Keras and InceptionResNetV2 Model)
- Image Catergorisation on image files that have gone through image classification. (via. gloVe)
