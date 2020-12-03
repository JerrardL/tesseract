import requests
import json
import time

from enrichments.Enrichment import Enrichment


class Categorisation(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Receives json reponse from classification as 'data'
        body = {
            "category_data": self.class_config["category_data"],
            "predictions": data
        }
        # If a classification was extracted, attempt to categorise the prediction via gloVe
        category = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        category_response = category.json()
        elapsed_time = time.time() - start_time
        category_response.update({"time_taken": elapsed_time})
        return category_response