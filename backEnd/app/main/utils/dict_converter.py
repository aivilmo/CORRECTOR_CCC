import json

# declaringa a class
class DictConverter:

    # constructor
    def __init__(self, dict):
        self.__dict__.update(dict)

    def convert(self, dict):
        return json.loads(json.dumps(dict), object_hook=DictConverter)
