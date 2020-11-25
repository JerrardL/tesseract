import requests

from enrichments.Enrichment import Enrichment


class DeepSpeech(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self, data):
        # Attempt to get speech recognition if audio file via DeepSpeech
        speech_response = requests.post(self.endpoint, data=data)
        extraction = speech_response.json()["text"]
        return extraction
