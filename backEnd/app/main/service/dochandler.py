"""--------------------------------"""
"""---- Manage Documents Class ----"""
"""--------------------------------"""

import re
import win32com.client
import glob
import os
from definitions import BASE_FOLDER, EXTENSION_LIST, IGNORED_EXERCISES
from configuration.logger import Logger
from configuration.app_config import AppConfig
from configuration.path_config import PathConfiguration


class DocHandler:

    # Instanciate the config
    AppConfig.getInstance().init_app_config()

    def __init__(self):
        self.logger = Logger()
        self.path = PathConfiguration.getInstance().config()
        self.PATH_EXERCISES = str(BASE_FOLDER.absolute()) + self.path.docx.exercises + "*."
        self.PATH_SOLUTIONS = str(BASE_FOLDER.absolute()) + self.path.docx.solutions + "*."

    
    def number_exercise(self, file_name):
        return int(file_name.split("_Ejercicio_")[1].split("_")[0])

    # Convert doc to docx
    def doc2docx(self, is_solution=False):
        self.logger.info("Converting doc documents to docx...")
        Word = win32com.client.Dispatch("Word.Application")
        Word.visible = 0
        path = self.PATH_EXERCISES
        if is_solution:
            path = self.PATH_SOLUTIONS
        for _, doc in enumerate(glob.iglob(path + EXTENSION_LIST[0])):
            in_file = os.path.abspath(doc)
            wb = Word.Documents.Open(in_file)
            out_file = os.path.abspath(in_file[:-4] + "." + EXTENSION_LIST[1])
            self.logger.info("Converting " + in_file + " to " + out_file + "...")
            try:
                wb.SaveAs2(out_file, FileFormat=16)  # file format for docx
            except Exception:
                self.logger.error("Error converting " + in_file + " to " + out_file + "\n" + Exception)
            wb.Close()
            os.remove(in_file)
        Word.Quit()

    # Extract response from the docx
    def clean_response(self, response, is_solution):
        responses = re.findall("[a-v]", response)
        if not is_solution:
            return responses
        else:
            return responses[:-4]

    # Get the list of the exercises downloaded
    def read_files(self, isSolution=False):
        solutions_list = []
        path = self.PATH_EXERCISES
        if isSolution:
            path = self.PATH_SOLUTIONS
        for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[1])):
            in_file = os.path.abspath(doc)
            num_exercise = self.number_exercise(in_file)
            if num_exercise not in IGNORED_EXERCISES:
                solutions_list.append(in_file)
        return solutions_list