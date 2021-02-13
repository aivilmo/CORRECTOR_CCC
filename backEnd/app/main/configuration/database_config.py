from utils.dict_converter import DictConverter


class DatabaseConfiguration:

    __instance = None

    def __init__(self, yaml_dict=None):
        if not yaml_dict is None:
            self.dict_converter = DictConverter(self.yaml_dict)
            self.db_config = self.dict_converter.convert(self.yaml_dict)

    # Singleton method
    def __new__(cls):
        if DatabaseConfiguration.__instance is None:
            DatabaseConfiguration.__instance = object.__new__(cls)
        return DatabaseConfiguration.__instance
