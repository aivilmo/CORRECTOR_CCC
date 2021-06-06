"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.bdconnection import DbManager
from rest.filedownloader import FileDownloader
from service.corrector import CorrectorManager
from service.dochandler import DocHandler


class MainClass:

    correctorManager = CorrectorManager()
    fileDownloader = FileDownloader()
    dbManager = DbManager()
    docHandler = DocHandler()

    def run(self):
        """----------------------------"""
        """----to correct exercises----"""
        """----------------------------"""
        self.fileDownloader.download_exercises()
        self.correctorManager.correct()
        """----------------------------------"""
        """----to pass the solutions to DB----"""
        """----------------------------------"""
        self.docHandler.doc2docx(True)
        solutions = self.docHandler.read_files(True)
        tuples_list = []
        for solution_file in solutions:
            number_of_exercise = self.docHandler.number_exercise(solution_file)
            response, num_questions = self.correctorManager.extract_solution_docx(
                solution_file
            )
            tuples_list.append(
                (solution_file, number_of_exercise, response, num_questions)
            )
        self.dbManager.post_solutions(tuples_list, password="harryna")


# Main
if __name__ == "__main__":
    MainClass().run()
