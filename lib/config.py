import yaml


class Config:
    __instance = None
    def __init__(self, configPath:str):
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self
        self.config = yaml.load(open(configPath), Loader=yaml.FullLoader)

    @staticmethod
    def getConfig():
        if Config.__instance is None:
            raise Exception("uninitialized singleton!")
        return Config.__instance.config
