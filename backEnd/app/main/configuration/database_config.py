from utils.dict_converter import DictConverter


class DatabaseConfiguration:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseConfiguration.__instance == None:
            DatabaseConfiguration()
        return DatabaseConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DatabaseConfiguration.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.dict_converter = None
            self.db_config = None
            DatabaseConfiguration.__instance = self

    def setConfiguration(self, yaml_dict):
        if not yaml_dict is None:
            self.dict_converter = DictConverter(yaml_dict)
            self.db_config = self.dict_converter.convert(yaml_dict)
            print(self.dict_converter)
            print(self.db_config)