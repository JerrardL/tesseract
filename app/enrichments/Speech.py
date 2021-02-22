import requests
import time

from enrichments.Enrichment import Enrichment


class Speech(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data, language):
        start_time = time.time()
        # Attempt to get speech recognition if audio file via CMU Sphinx
        speech_response = requests.post(self.endpoint, data=data, params={"language": language})
        extraction = speech_response.json()
        elapsed_time = time.time() - start_time
        return {"extraction": extraction, "time_taken": elapsed_time}
