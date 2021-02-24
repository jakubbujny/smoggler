import logging

import yaml

from lib.logger import logger


class Config:
    __instance = None
    def __init__(self, configPath:str):
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self
        logger.info(f"Loading config from {configPath}")
        self.config = yaml.load(open(configPath), Loader=yaml.FullLoader)
        self.configPath = configPath

    @staticmethod
    def getConfig():
        if Config.__instance is None:
            raise Exception("uninitialized singleton!")
        return Config.__instance.config

    def saveConfig(self):
        logger.info(f"Saving config to {self.configPath}")
        with open(self.configPath, 'w') as yaml_file:
            yaml.dump(self.config, yaml_file, default_flow_style=False)
