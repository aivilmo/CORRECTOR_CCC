"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from service.bdconnection import DbManager
from service.webscrapper import *
from service.corrector import CorrectorManager

# Main
if __name__ == "__main__":
    """----------------------------"""
    """----to correct exercises----"""
    """----------------------------"""
    #initExplorer()
    #login()
    #downloadOpenDocs()
    CorrectorManager().correct()
    """----------------------------------"""
    """----to pass the solutions to DB----"""
    """----------------------------------"""
    """
    doc2docx(True)
    solutions = read_files(True)
    DbManager().post_solutions(solutions, password="harryna")
    """
