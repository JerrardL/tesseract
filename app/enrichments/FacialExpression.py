import requests
import time

from enrichments.Enrichment import Enrichment

class FacialExpression(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self,data):
        start_time = time.time()
        # Facial Expression
        expression_response = requests.post(self.endpoint, data=data)
        expression_extraction = expression_response.json()
        elapsed_time = time.time() - start_time
        expression_extraction.update({"time_taken": elapsed_time})
        return expression_extraction