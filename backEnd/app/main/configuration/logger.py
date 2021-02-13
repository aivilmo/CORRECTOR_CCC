import logging


class Logger:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            logging.basicConfig(
                level=logging.DEBUG,
                filename="data/logger/app.log",
                filemode="w",
                format="[%(levelname)s] %(name)s: %(message)s",
            )
            self.logger = logging.getLogger()
            Logger.__instance = self

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