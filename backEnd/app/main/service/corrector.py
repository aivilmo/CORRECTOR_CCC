"""---------------------------"""
"""----- Corrector Class -----"""
"""---------------------------"""


import docx
import os
from docx.shared import RGBColor
from service.bdconnection import DbManager
from service.dochandler import DocHandler
from definitions import IGNORED_EXERCISES, INDEX_CALIFICATION, INDEX_COMMENTARY
from configuration.logger import Logger


class CorrectorManager:

    docHandler = DocHandler()
    dbManager = DbManager()

    def __init__(self):
        self.logger = Logger()

    # Read responses and correct the docx
    def correct_exercise_docx(self, filename):
        num_exercise = self.docHandler.number_exercise(filename)
        if num_exercise in IGNORED_EXERCISES:
            self.logger.info("Ignoring " + filename)
            return
        try:
            document = docx.Document(filename)
            responses = dict()
            question = 1
            wrong_answer = 0
            solution = self.dbManager.get_solutions(num_exercise)
            if solution == []:
                self.logger.warning(
                    "No solution in DB to exercise " + str(num_exercise)
                )
                return
            solution = solution[0][0]
            solution_keys = list(solution.keys())
            for paragraph in document.paragraphs:
                paragraph_text = paragraph.text
                index = paragraph_text.find("La respuesta es")
                if index != -1:
                    response = paragraph_text.split(":")
                    responses[question] = self.docHandler.clean_response(
                        response[1].lower(), False
                    )
                    solution_key = solution_keys[question - 1]
                    if set(responses[question]) != set(solution[solution_key]):
                        wrong_answer += 1
                        correction = paragraph.add_run(solution[solution_key])
                    else:
                        correction = paragraph.add_run(" bien")
                    self.set_style(correction)
                    question += 1
            if question == 1:
                self.logger.error("Error reading responses " + filename)
                return
            question -= 1
            grade = round(((question - wrong_answer) * 10) / question, 2)
            self.logger.info(filename)
            self.logger.info("Grade: " + str(grade))
            grade_str = document.paragraphs[INDEX_CALIFICATION].add_run(str(grade))
            commentary = self.generate_commentary(grade)
            commentary_str = document.paragraphs[INDEX_COMMENTARY].add_run(commentary)
            self.set_style(grade_str)
            self.set_style(commentary_str)
        except Exception as e:
            self.logger.error("Error in file " + filename + "\n" + str(e))
            return
        document.save(filename[:-5] + "_CORREGIDO.docx")
        os.remove(filename)
        return responses, question - 1

    # Set read letters to correct the docx
    def set_style(self, paragraph):
        paragraph.bold = True
        paragraph.font.color.rgb = RGBColor(255, 0, 0)

    # Generate commentary from the docx
    def generate_commentary(self, grade):
        if grade <= 5:
            return "Muy flojo"
        elif grade > 5 and grade <= 6:
            return "Bien"
        elif grade > 6 and grade <= 8:
            return "Muy bien"
        elif grade > 8:
            return "Excelente"
        elif grade == 10:
            return "Enhorabuena"

    # Extract response from the solution docx
    def extract_solution_docx(self, filename):
        try:
            document = docx.Document(filename)
            responses = dict()
            question = 1
            for paragraph in document.paragraphs:
                paragraph_text = paragraph.text
                index = paragraph_text.find("La respuesta es")
                if index == -1:
                    index = paragraph_text.find("La respuesta correcta es")
                if index != -1:
                    response = paragraph_text.split(":")
                    responses[question] = self.docHandler.clean_response(
                        response[1].lower(), True
                    )
                    question += 1
        except Exception as e:
            self.logger.error("Error in file " + filename + "\n" + str(e))
            return
        return responses, question - 1

    # Correct all exercises in the path
    def correct(self):
        self.docHandler.doc2docx()
        self.logger.info("Correcting exercises...\n")
        for doc in self.docHandler.read_files():
            self.correct_exercise_docx(doc)
