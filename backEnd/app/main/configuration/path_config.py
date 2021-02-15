from utils.dict_converter import DictConverter


class PathConfiguration:

    __instance = None
    dict_converter = None
    routes = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PathConfiguration.__instance == None:
            PathConfiguration()
        return PathConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PathConfiguration.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PathConfiguration.__instance = self

    def setConfiguration(self, yaml_dict):
        self.dict_converter = DictConverter(yaml_dict)
        self.routes = self.dict_converter.convert(yaml_dict)