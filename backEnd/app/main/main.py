"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.bdconnection import DbManager
from service.webscrapper import WebScrapper
from service.corrector import CorrectorManager
from service.dochandler import DocHandler

class MainClass:

    correctorManager = CorrectorManager()
    webScrapper = WebScrapper()
    dbManager = DbManager()
    docHandler = DocHandler()

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
        tuples_list = []
        for solution_file in solutions:
            number_of_exercise = self.docHandler.number_exercise(solution_file)
            response, num_questions = self.correctorManager.extract_solution_docx(solution_file)
            tuples_list.append((solution_file, number_of_exercise, response, num_questions))
        self.dbManager.post_solutions(tuples_list, password="harryna")

# Main
if __name__ == "__main__":
    MainClass().run()

