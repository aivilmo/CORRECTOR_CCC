"""---------------------------"""
"""----- Corrector Class -----"""
"""---------------------------"""


import docx
import re
import win32com.client
import glob
import os
from docx.shared import RGBColor
from service.bdconnection import *
from definitions import BASE_FOLDER



class CorrectorManager:
    
    #const
    EXTENSION_LIST = ["doc", "docx", "odt", "pdf"]
    IGNORED_EXERCISES = [7, 8, 9, 12, 13]  # Nat = 7, 8, 9 | FB = 12, 13
    INDEX_CALIFICATION = 10
    INDEX_COMMENTARY = 11

    def __init__(self):
        pass

    def number_exercise(self, file_name):
        return int(file_name.split("_Ejercicio_")[1].split("_")[0])

# Convert doc to docx
    def doc2docx(self, is_solution=False):
        Word = win32com.client.Dispatch("Word.Application")
        Word.visible = 0
        path = str(BASE_FOLDER.absolute()) + "\\data\\storage\\exercises\\*."
        if is_solution:
            path = "Soluciones\*."
        for i, doc in enumerate(glob.iglob(path + self.EXTENSION_LIST[0])):
            in_file = os.path.abspath(doc)
            wb = Word.Documents.Open(in_file)
            out_file = os.path.abspath(in_file[:-4] + "." + self.EXTENSION_LIST[1])
            print("Converting " + in_file + " to " + out_file + "...")
            print("")
            wb.SaveAs2(out_file, FileFormat=16)  # file format for docx
            wb.Close()
            os.remove(in_file)
        Word.Quit()

    # Extract response from the docx
    def clean_response(self, response, is_solution):
        responses = re.findall("[a-v]", response)
        if (not is_solution):
            return responses
        else:
            return responses[:-4]

    # Read responses and correct the docx
    def correct_exercise_docx(self, filename):
        num_exercise = self.number_exercise(filename)
        if (num_exercise in self.IGNORED_EXERCISES):
            print("Ignoring " + filename)
            return
        try:
            document = docx.Document(filename)
            responses = dict()
            question = 1
            wrong_answer = 0
            solution = DbManager().get_solutions(num_exercise)
            if (solution == []):
                print("No solution in DB to exercise " + str(num_exercise))
                return
            solution = solution[0][0]
            solution_keys = list(solution.keys())
            for paragraph in document.paragraphs:
                paragraph_text = paragraph.text
                index = paragraph_text.find("La respuesta es")
                if (index != -1):
                    response = paragraph_text.split(":")
                    responses[question] = self.clean_response(response[1].lower(), False)
                    solution_key = solution_keys[question - 1]
                    if (set(responses[question]) != set(solution[solution_key])):
                        wrong_answer += 1
                        correction = paragraph.add_run(solution[solution_key])
                    else:
                        correction = paragraph.add_run(" bien")
                    self.set_style(correction)
                    question += 1
            if (question == 1):
                print("Error reading responses " + filename)
                return
            question -= 1
            grade = round(((question - wrong_answer) * 10) / question, 2)
            print(filename)
            print("Grade: " + str(grade))
            print("")
            grade_str = document.paragraphs[self.INDEX_CALIFICATION].add_run(str(grade))
            commentary = self.generate_commentary(grade)
            commentary_str = document.paragraphs[self.INDEX_COMMENTARY].add_run(commentary)
            self.set_style(grade_str)
            self.set_style(commentary_str)
        except Exception as e:
            print("Error in file " + filename)
            print(str(e))
        document.save(filename[:-5] + "_CORREGIDO.docx")
        os.remove(filename)
        return responses, question - 1

    # Set read letters to correct the docx
    def set_style(self, paragraph):
        paragraph.bold = True
        paragraph.font.color.rgb = RGBColor(255, 0, 0)

    # Generate commentary from the docx
    def generate_commentary(self, grade):
        if (grade <= 5):
            return "Muy flojo"
        elif (grade > 5 and grade <= 6):
            return "Bien"
        elif (grade > 6 and grade <= 8):
            return "Muy bien"
        elif (grade > 8):
            return "Excelente"
        elif (grade == 10):
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
                    responses[question] = self.clean_response(response[1].lower(), True)
                    question += 1
        except Exception as e:
            print("Error in file " + filename)
            print(str(e))
        return responses, question - 1

    # Get the list of the exercises downloaded
    def read_files(self, isSolution=False):
        solutions_list = []
        path = str(BASE_FOLDER.absolute()) + "\\data\\storage\\exercises\\*."
        if isSolution:
            path = "..\..\EJERCICIOS_CCC\Soluciones\*."
        for i, doc in enumerate(glob.iglob(path + self.EXTENSION_LIST[1])):
            in_file = os.path.abspath(doc)
            num_exercise = self.number_exercise(in_file)
            if num_exercise not in self.IGNORED_EXERCISES:
                solutions_list.append(in_file)
        return solutions_list

    # Correct all exercises in the path
    def correct(self):
        self.doc2docx()
        print("Correcting exercises...")
        print("")
        for doc in self.read_files():
            self.correct_exercise_docx(doc)
