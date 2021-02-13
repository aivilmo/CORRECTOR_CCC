import yaml
from configuration.ccc_config import CCCConfiguration
from configuration.path_config import PathConfiguration
from configuration.database_config import DatabaseConfiguration


class AppConfig:

    FILE_URL = "data/env_config/app.yaml"
    __instance = None

    def __init__(self):
        self.yaml_dict = self.read_configuration_file()
        self.init_configurations(yaml_dict)

    # Singleton method
    def __new__(cls):
        if AppConfig.__instance is None:
            AppConfig.__instance = object.__new__(cls)
        return AppConfig.__instance

    def read_configuration_file(self):
        with open(self.FILE_URL) as file:
            document = yaml.load(file, Loader=yaml.FullLoader)
        return document

    def init_configurations(yaml_dict):
        DatabaseConfiguration(yaml_dict["database"])
        CCCConfiguration(yaml_dict["ccc"])
        PathConfiguration(yaml_dict["path"])
