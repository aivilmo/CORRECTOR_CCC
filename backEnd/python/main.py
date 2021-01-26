"""--------------------"""
"""---- Main Class ----"""
"""--------------------"""

from configuration.lib import *

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
    """
    doc2docx(True)
    solutions = read_files(True)
    post_solutions(solutions, password="harryna")
    """
