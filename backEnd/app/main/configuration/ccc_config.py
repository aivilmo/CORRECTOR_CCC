from utils.dict_converter import DictConverter


class CCCConfiguration:

    __instance = None

    def __init__(self, yaml_dict=None):
        if not yaml_dict is None:
            self.dict_converter = DictConverter(self.yaml_dict)
            self.ccc = self.dict_converter.convert(self.yaml_dict)

    # Singleton method
    def __new__(cls):
        if CCCConfiguration.__instance is None:
            CCCConfiguration.__instance = object.__new__(cls)
        return CCCConfiguration.__instance