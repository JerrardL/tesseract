import requests
import json

from enrichments.Enrichment import Enrichment


class NLP(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # If text was extracted from the file, attempt to perform nlp via Scapy
        body = {'text': data, 'model': 'en'}
        nlp_response = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        nlp_extraction = nlp_response.json()
        return nlp_extraction
