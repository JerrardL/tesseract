import requests
import time

from enrichments.Enrichment import Enrichment

class Video(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Attempt to convert video to audio and then perform speech recognition via DeepSpeech
        video_response = requests.post(self.endpoint, data=data)
        video_extraction = video_response.json()["text"]
        elapsed_time = time.time() - start_time
        return {"extraction": video_extraction, "time_taken": elapsed_time}