
from definitions import BASE_FOLDER
import yaml

class AppConfig:

    __instance = None
    CONFIGURATION_FILE= str(BASE_FOLDER.absolute()) + "\\app.yaml"

    # Singleton method
    def __new__(cls):
        if AppConfig.__instance is None:
            AppConfig.__instance = object.__new__(cls)
        return AppConfig.__instance

    def __init__(self):
        with open(self.CONFIGURATION_FILE) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            self.ccc_config = self.config["ccc"]
            self.docx_path_config = self.config["path"]["docx"]
            self.database_config = self.config["database"]

    # get config ccc
    def ccc_url(self):
        return self.ccc_config["url"]

    def ccc_username(self):
        return self.ccc_config["username"]

    def ccc_password(self):
        return self.ccc_config["password"]

    # get config path docx
    def path_docx_exercises(self):
        return self.docx_path_config["exercises"]

    def path_docx_solutions(self):
        return self.docx_path_config["solutions"]

    # get config database
    def database_host(self):
        return self.database_config["host"]

    def database_name(self):
        return self.database_config["name"]

    def database_user(self):
        return self.database_config["user"]

    def database_password(self):
        return self.database_config["password"]