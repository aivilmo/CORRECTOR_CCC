"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.corrector import *
from service.bdconnection import *
from service.webscrapper import *

# Main
if __name__ == "__main__":
    """----------------------------"""
    """----to correct exercises----"""
    """----------------------------"""
    initExplorer()
    login()
    downloadOpenDocs()
    correct()
    """----------------------------------"""
    """----to pass the solutions to DB----"""
    """----------------------------------"""
    doc2docx(True)
    solutions = read_files(True)
    tuples_list = []
    for solution_file in solutions:
        number_of_exercise = number_exercise(solution_file)
        response, num_questions = extract_solution_docx(solution_file)
        tuples_list.append((solution_file, number_of_exercise, response, num_questions))
    post_solutions(tuples_list, password="harryna")
