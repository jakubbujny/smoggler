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

    @staticmethod
    def getConfig():
        if Config.__instance is None:
            raise Exception("uninitialized singleton!")
        return Config.__instance.config
