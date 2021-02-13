from utils.dict_converter import DictConverter


class CCCConfiguration:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CCCConfiguration.__instance == None:
            CCCConfiguration()
        return CCCConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CCCConfiguration.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.dict_converter = None
            self.ccc_config = None
            CCCConfiguration.__instance = self

    def setConfiguration(self, yaml_dict):
        if not yaml_dict is None:
            self.dict_converter = DictConverter(yaml_dict)
            self.ccc_config = self.dict_converter.convert(yaml_dict)
