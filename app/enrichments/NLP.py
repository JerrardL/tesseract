import requests
import json
import time

from enrichments.Enrichment import Enrichment


class NLP(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # If text was extracted from the file, attempt to perform nlp via Scapy
        body = {'text': data, 'model': 'en'}
        nlp_response = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        nlp_extraction = nlp_response.json()
        elapsed_time = time.time() - start_time
        nlp_extraction.update({"time_taken": elapsed_time})
        return nlp_extraction
