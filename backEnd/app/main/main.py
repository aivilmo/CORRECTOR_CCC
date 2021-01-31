"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.bdconnection import DbManager
from service.webscrapper import WebScrapper
from service.corrector import CorrectorManager

# Main
if __name__ == "__main__":
    correctorManager = CorrectorManager()
    webScrapper = WebScrapper()
    dbManager = DbManager()
    """----------------------------"""
    """----to correct exercises----"""
    """----------------------------"""
    webScrapper.init_explorer()
    webScrapper.login()
    webScrapper.download_docs()
    correctorManager.correct()
    """----------------------------------"""
    """----to pass the solutions to DB----"""
    """----------------------------------"""
    correctorManager.doc2docx(True)
    solutions = correctorManager.read_files(True)
    tuples_list = []
    for solution_file in solutions:
        number_of_exercise = correctorManager.number_exercise(solution_file)
        response, num_questions = correctorManager.extract_solution_docx(solution_file)
        tuples_list.append((solution_file, number_of_exercise, response, num_questions))
    dbManager.post_solutions(tuples_list, password="harryna")

