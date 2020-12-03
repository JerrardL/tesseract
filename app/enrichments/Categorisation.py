import requests
import json

from enrichments.Enrichment import Enrichment


class Categorisation(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Receives json reponse from classification as 'data'
        body = {
            "category_data": self.class_config["category_data"],
            "predictions": data
        }
        # If a classification was extracted, attempt to categorise the prediction via gloVe
        category = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        category_response = category.json()
        return category_response