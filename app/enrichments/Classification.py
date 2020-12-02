import requests

from enrichments.Enrichment import Enrichment


class Classification(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to classify the image via keras
        classification_response = requests.post(self.endpoint, data=data)
        classification_extraction = classification_response.json()
        return classification_extraction