import requests
import json
import time

from enrichments.Enrichment import Enrichment

class ImageAICategorisation(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Receives reponse from video_or as 'data'
        length = len(data)
        if length == 0:
            object_predictions = None
        else:
            object_predictions = {
                "Best Prediction": data[0][0]
            }
        if length > 1:
            object_predictions["Mid Prediction"] = data[1][0]
        if length > 2:
            object_predictions["Low Prediction"] = data[2][0]


        body = {
            "category_data": self.class_config["category_data"],
            "predictions": object_predictions
        }
        # If a classification was extracted, attempt to categorise the prediction via gloVe
        category = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        category_response = category.json()
        elapsed_time = time.time() - start_time
        category_response.update({"time_taken": elapsed_time})
        return category_response
