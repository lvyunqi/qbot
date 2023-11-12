import os
from botpy.ext.cog_yaml import read

class Config:
    def __init__(self):
        self.path = os.getcwd()
    
    def config(self):
        return read(os.path.join(self.path, "config.yaml"))