from utils.dict_converter import DictConverter
from exception.singleton_exception import SingletonException


class DatabaseConfiguration:

    __instance = None
    dict_converter = None
    db_config = None
    yaml = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseConfiguration.__instance == None:
            DatabaseConfiguration()
        return DatabaseConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DatabaseConfiguration.__instance != None:
            raise SingletonException
        else:
            DatabaseConfiguration.__instance = self

    def setConfiguration(self, yaml_dict):
        self.dict_converter = DictConverter(yaml_dict)
        self.db_config = self.dict_converter.convert(yaml_dict)