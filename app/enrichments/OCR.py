import requests
import time

from enrichments.Enrichment import Enrichment


class OCR(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Attempt to get speech recognition if audio file via DeepSpeech
        ocr_response = requests.put(self.endpoint, data=data)
        extraction = ocr_response.text.replace('\n', ' ')
        elapsed_time = time.time() - start_time
        return {"ocr_extraction": extraction, "time_taken": elapsed_time}

