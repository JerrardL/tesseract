import requests
import time

from enrichments.Enrichment import Enrichment


class NewSpeech(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Attempt to get speech recognition if audio file via CMU Sphinx
        speech_response = requests.post(self.endpoint, data=data)
        extraction = speech_response.json()["text"]
        elapsed_time = time.time() - start_time
        return {"extraction": extraction, "time_taken": elapsed_time}
