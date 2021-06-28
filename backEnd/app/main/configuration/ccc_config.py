from utils.dict_converter import DictConverter
from exception.singleton_exception import SingletonException


class CCCConfiguration:

    __instance = None
    dict_converter = None
    ccc_config = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CCCConfiguration.__instance == None:
            CCCConfiguration()
        return CCCConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CCCConfiguration.__instance != None:
            raise SingletonException
        else:
            CCCConfiguration.__instance = self

    def setConfiguration(self, yaml_dict):
        self.dict_converter = DictConverter(yaml_dict)
        self.ccc_config = self.dict_converter.convert(yaml_dict)

    def config(self):
        return self.ccc_config
