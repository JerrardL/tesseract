import requests
import time

from enrichments.Enrichment import Enrichment


class Captioning(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to perform image captioning via Tensorflow
        start_time = time.time()
        form_data = {'image': data}
        captioning_response = requests.post(self.endpoint, files=form_data)
        captioning_extraction = captioning_response.json()
        elapsed_time = time.time() - start_time
        # FILTERING RESPONSES
        # valid_captioning = []
        # for caption in captioning_extraction['predictions']:
        #     if caption['probability'] > self.class_config['probability_threshold']:
        #         valid_captioning.append(caption)
        captioning_extraction.update({"time_taken": elapsed_time})
        return captioning_extraction
