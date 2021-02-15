import yaml
from configuration.ccc_config import CCCConfiguration
from configuration.path_config import PathConfiguration
from configuration.database_config import DatabaseConfiguration


class AppConfig:

    FILE_URL = "data/env_config/app.yaml"

    __instance = None
    yaml_dict = None

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
            self.__database = DatabaseConfiguration.getInstance()
            self.__path = PathConfiguration.getInstance()
            self.__ccc = CCCConfiguration.getInstance()
            AppConfig.__instance = self

    def load_configuration(app_conf_call):
        def add_init_config(self):
            AppConfig.getInstance().init_app_config()
            app_conf_call(self)

        return add_init_config

    def read_configuration_file(self):
        with open(self.FILE_URL) as file:
            document = yaml.load(file, Loader=yaml.FullLoader)
        return document

    def init_app_config(self):
        self.yaml_dict = self.read_configuration_file()
        self.init_configurations(self.yaml_dict)

    def init_configurations(self, yaml_dict):
        self.__database.setConfiguration(yaml_dict["database"])
        self.__ccc.setConfiguration(yaml_dict["ccc"])
        self.__path.getInstance().setConfiguration(yaml_dict["path"])
