import requests

from enrichments.Enrichment import Enrichment


class Captioning(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to perform image captioning via Tensorflow
        form_data = {'image': data}
        captioning_response = requests.post(self.endpoint, files=form_data)
        captioning_extraction = captioning_response.json()
        valid_captioning = []
        for caption in captioning_extraction['predictions']:
            if caption['probability'] > self.class_config['probability_threshold']:
                valid_captioning.append(caption)
        return valid_captioning
