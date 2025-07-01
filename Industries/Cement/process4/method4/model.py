__package__ = "industry.process.method1"

import os
from idr_iisim.models.model import Model


class MethodModel(Model):
    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.model_config = self.directory + "/meta.yaml"
        self.setup()
        pass

    pass
