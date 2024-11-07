# framework/data_access/config.py

import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.config = {}
        load_dotenv()

    def get_config(self, config_name):
        return self.config.get(config_name) or os.getenv(config_name)

    def set_config(self, config_name, config_value):
        self.config[config_name] = config_value
