import requests
import time

from enrichments.Enrichment import Enrichment


class KerasClassification(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to classify the image via keras
        start_time = time.time()
        classification_response = requests.post(self.endpoint, data=data)
        classification_extraction = classification_response.json()
        elapsed_time = time.time() - start_time
        classification_extraction.update({"time_taken": elapsed_time})
        return classification_extraction