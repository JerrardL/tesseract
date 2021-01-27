import requests
import time
import json

from enrichments.Enrichment import Enrichment

class TextSentimentAnalysis(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        info = "Sentiment results below are based on percentages, with scores closer to 1 representing a stronger likelihood of whether text is positive, neutral or negative. " \
                "Compound uses a different measurement. It is a summation of valence scores of each word in the lexicon, normalised to values between -1 being most extreme " \
                "negative, and 1 being most extreme positive. The idea is that you can have have an overall positive sentiment, which may contain stronger classed negative words, " \
                "but not enough to change the overall text sentiment."

        start_time = time.time()
        body = {'text': data}
        sentiment_response = requests.post(self.endpoint, data=json.dumps(body), headers=self.headers)
        sentiment_extraction = sentiment_response.json()["text"]
        elapsed_time = time.time() - start_time
        sentiment_extraction = {"info": info, "sentiment_analysis": sentiment_extraction, "time_taken": elapsed_time}
        return sentiment_extraction