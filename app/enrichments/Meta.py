import requests

from enrichments.Enrichment import Enrichment


class Meta(Enrichment):

    def __init__(self, config):
        super().__init__(config)
        super().set_config(self.__class__.__name__)

    def execute(self,data):
        # Send file through to Tika for metadata
        resp_meta = requests.put(self.endpoint, data=data, headers=self.headers)
        meta = resp_meta.json()
        return meta
