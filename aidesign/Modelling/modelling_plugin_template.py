import numpy as np
import pandas as pd

class ModellingPluginTemplate(object):
    def __init__(self) -> None:
        self.X = None
        self.Y = None
        self.X_tst = None
        self.Y_tst = None