import logging


class Logger:

    __instance = None
    nombre = None

    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="app.log",
            filemode="w",
            format="[%(levelname)s] %(name)s: %(message)s",
        )
        self.logger = logging.getLogger()

    # Singleton method
    def __new__(cls):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
        return Logger.__instance

    def debug(self, message):
        print("[DEBUG]: " + message)
        self.logger.debug(message)

    def info(self, message):
        print("[INFO]: " + message)
        self.logger.info(message)

    def warning(self, message):
        print("[WARNING]: " + message)
        self.logger.warning(message)

    def error(self, message):
        print("[ERROR]: " + message)
        self.logger.error(message)

    def critical(self, message):
        print("[CRITICAL]: " + message)
        self.logger.critical(message)