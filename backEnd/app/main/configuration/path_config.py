from utils.dict_converter import DictConverter


class PathConfiguration:

    __instance = None

    def __init__(self, yaml_dict=None):
        if not yaml_dict is None:
            self.dict_converter = DictConverter(self.yaml_dict)
            self.route = self.dict_converter.convert(self.yaml_dict)

    # Singleton method
    def __new__(cls):
        if PathConfiguration.__instance is None:
            PathConfiguration.__instance = object.__new__(cls)
        return PathConfiguration.__instance