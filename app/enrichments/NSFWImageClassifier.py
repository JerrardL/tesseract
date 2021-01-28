import requests
import time

from enrichments.Enrichment import Enrichment

class NSFWImageClassifier(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self,data):
        info = "Resutls show a percentage value estimation of whether the image can be seen as suitable (safe) or explicit (unsafe) for viewing at work."


        start_time = time.time()
        # Send file through to Nudenet for classification
        classifier_response = requests.post(self.endpoint, data=data)
        classifier = {"info": info}
        classifier.update(classifier_response.json())
        elapsed_time = time.time() - start_time
        classifier.update({"time_taken": elapsed_time})
        return classifier