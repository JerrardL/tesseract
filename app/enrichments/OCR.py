import requests

from enrichments.Enrichment import Enrichment


class OCR(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to get speech recognition if audio file via DeepSpeech
        ocr_response = requests.put(self.endpoint, data=data)
        extraction = ocr_response.text.replace('\n', ' ')
        return extraction

