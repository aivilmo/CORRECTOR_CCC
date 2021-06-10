"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from configuration.app_config import AppConfig
from service.bdconnection import DbManager
from service.webscrapper import WebScrapper
from service.corrector import CorrectorManager
from service.dochandler import DocHandler


class MainClass:
    def __init__(self):
        self.correctorManager = CorrectorManager()
        self.webScrapper = WebScrapper()
        self.dbManager = DbManager()
        self.docHandler = DocHandler()

    def run(self):
        """----------------------------"""
        """----to correct exercises----"""
        """----------------------------"""
        self.webScrapper.init_explorer()
        self.webScrapper.login()
        self.webScrapper.download_docs()
        self.correctorManager.correct()
        """----------------------------------"""
        """----to pass the solutions to DB----"""
        """----------------------------------"""
        self.docHandler.doc2docx(True)
        solutions = self.docHandler.read_files(True)
        tuples_list = self.correctorManager.get_data_to_save(solutions)
        self.dbManager.post_solutions(tuples_list)


# Main
if __name__ == "__main__":
    MainClass().run()
