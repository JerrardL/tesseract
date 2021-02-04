import requests
import time
import json

from enrichments.Enrichment import Enrichment

class TextSentimentAnalysis(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        body = {'text': data}
        sentiment_response = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        sentiment_extraction = sentiment_response.json()["text"]
        elapsed_time = time.time() - start_time
        sentiment_extraction = {"sentiment_analysis": sentiment_extraction, "time_taken": elapsed_time}
        return sentiment_extraction