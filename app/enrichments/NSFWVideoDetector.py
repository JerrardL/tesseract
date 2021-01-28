import requests
import time

from enrichments.Enrichment import Enrichment

class NSFWVideoDetector(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self,data):
        start_time = time.time()
        # Send file through to Nudenet for detection
        detection_response = requests.post(self.endpoint, data=data)
        detection = detection_response.json()
        elapsed_time = time.time() - start_time
        detection.update({"time_taken": elapsed_time})
        return detection