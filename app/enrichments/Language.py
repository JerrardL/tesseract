import requests
import json
import time

from enrichments.Enrichment import Enrichment

class Language(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        body = {'text': data}
        language_response = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        language_extraction = language_response.json()["text"]
        elapsed_time = time.time() - start_time
        language_extraction = {"language": language_extraction, "time_taken": elapsed_time}
        return language_extraction
