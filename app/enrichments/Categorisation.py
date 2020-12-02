import requests

from enrichments.Enrichment import Enrichment


class Categorisation(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # If a classification was extracted, attempt to categorise the prediction via gloVe
        classification_response = requests.post(self.endpoint, data=data)
        pass