"""--------------------------------"""
"""---- Manage Documents Class ----"""
"""--------------------------------"""

import re
import win32com.client
import glob
import os
from configuration.app_config import AppConfig
from configuration.path_config import PathConfiguration
from definitions import BASE_FOLDER, EXTENSION_LIST, IGNORED_EXERCISES
from configuration.logger import Logger


class DocHandler:
    @AppConfig.load_configuration
    def __init__(self):
        self.logger = Logger.getInstance()
        self.config_path = PathConfiguration.getInstance().routes
        self.PATH_EXERCISES = str(BASE_FOLDER.absolute()) + self.config_path.docx.exercises
        self.PATH_SOLUTIONS = str(BASE_FOLDER.absolute()) + self.config_path.docx.solutions

    def number_exercise(self, file_name):
        return int(file_name.split("_Ejercicio_")[1].split("_")[0])

    # Convert doc to docx
    def doc2docx(self, is_solution=False):
        Word = win32com.client.Dispatch("Word.Application")
        Word.visible = 0
        path = self.get_path(is_solution)
        for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[0])):
            in_file = os.path.abspath(doc)
            wb = Word.Documents.Open(in_file)
            out_file = os.path.abspath(in_file[:-4] + "." + EXTENSION_LIST[1])
            self.logger.info("Converting " + in_file + " to " + out_file + "...")
            wb.SaveAs2(out_file, FileFormat=16)  # file format for docx
            wb.Close()
            os.remove(in_file)
        Word.Quit()

    # Extract response from the docx
    def clean_response(self, response, is_solution):
        responses = re.findall("[a-v]", response)
        return responses if not is_solution else responses[:4]

    # Get the list of the exercises downloaded
    def read_files(self, is_solution=False):
        solutions_list = []
        path = self.get_path(is_solution)
        for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[1])):
            in_file = os.path.abspath(doc)
            num_exercise = self.number_exercise(in_file)
            if num_exercise not in IGNORED_EXERCISES:
                solutions_list.append(in_file)
        return solutions_list

    def get_path(self, is_solution):
        return self.PATH_EXERCISES if is_solution else self.PATH_SOLUTIONS