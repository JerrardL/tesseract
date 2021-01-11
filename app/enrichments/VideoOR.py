import requests
import time

from enrichments.Enrichment import Enrichment

class VideoOR(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        start_time = time.time()
        # Attempt to convert video to audio and then perform speech recognition via DeepSpeech
        video_response = requests.post(self.endpoint, data=data)
        video_extraction = video_response.json()
        elapsed_time = time.time() - start_time
        video_response.update({"time_taken": elapsed_time})
        return video_extraction