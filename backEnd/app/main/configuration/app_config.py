import yaml
from configuration.ccc_config import CCCConfiguration
from configuration.path_config import PathConfiguration
from configuration.database_config import DatabaseConfiguration


class AppConfig:

    FILE_URL = "data/env_config/app.yaml"

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AppConfig.__instance == None:
            AppConfig()
        return AppConfig.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AppConfig.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.yaml_dict = None
            AppConfig.__instance = self

    def read_configuration_file(self):
        with open(self.FILE_URL) as file:
            document = yaml.load(file, Loader=yaml.FullLoader)
        return document

    def init_app_config(self):
        self.yaml_dict = self.read_configuration_file()
        self.init_configurations(self.yaml_dict)

    def init_configurations(self, yaml_dict):
        DatabaseConfiguration.getInstance().setConfiguration(yaml_dict["database"])
        CCCConfiguration.getInstance().setConfiguration(yaml_dict["ccc"])
        PathConfiguration.getInstance().setConfiguration(yaml_dict["path"])
