class Enrichment:

    def __init__(self, config):
        self.config = config

    def set_config(self, name):
        self.class_config = self.config["enrichments"][name]
        self.supported_types = self.class_config["supported_types"]
        self.endpoint = self.class_config["endpoint"]
        self.headers = self.class_config["headers"]

    def execute(self, data):
        pass
