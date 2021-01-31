"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.corrector import *
from service.bdconnection import *

# Main
if __name__ == "__main__":
    """----------------------------"""
    """----to correct exercises----"""
    """----------------------------"""
    # initExplorer()
    # login()
    # downloadOpenDocs()
    correct()
    """----------------------------------"""
    """----to pass the solutions to DB----"""
    """----------------------------------"""
    doc2docx(True)
    solutions = read_files(True)
    tuples_list = []
    for solution_file in solutions:
        response, num_questions = extract_solution_docx(solution_file)
        tuples_list.append((solution_file, response, num_questions))
    post_solutions(tuples_list, password="harryna")
