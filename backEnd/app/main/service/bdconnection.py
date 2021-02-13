"""-----------------------------"""
"""---- Class to connect DB ----"""
"""-----------------------------"""

import psycopg2
import json
from configuration.logger import Logger
from configuration.database_config import DatabaseConfiguration


class DbManager:
    def __init__(self):
        self.config = DatabaseConfiguration.getInstance().db_config
        self.logger = Logger.getInstance()

    def connect_db(self):
        print(self.config)
        connection = psycopg2.connect(
            host=self.config.host,
            database=self.config.name,
            user=self.config.user,
            password=self.config.password,
        )
        connection.autocommit = True
        return connection

    def disconnect_db(self, connection):
        connection.close()

    # Get solutions from the db for a excercise id
    def get_solutions(self, exercise_id):
        connection = self.connect_db()
        query = connection.cursor()
        query.execute(
            "SELECT solutions_list FROM solutions WHERE exercise=" + str(exercise_id)
        )
        solution = query.fetchall()
        self.disconnect_db(connection)
        return solution

    # Write the solutions in db
    def post_solutions(self, exercise_data_tuple_list):
        connection = self.connect_db()
        self.logger.info("Inserting solutions in db...")
        query = connection.cursor()
        filename_list = []
        for tuple_item in exercise_data_tuple_list:
            filename, number_of_exercise, response, num_questions = tuple_item
            filename_list.append(filename)
            args = (num_questions, number_of_exercise, json.dumps(response))
            sql = "INSERT INTO public.solutions(num_questions, exercise, solutions_list) VALUES {} ON CONFLICT (exercise) DO NOTHING ".format(
                args
            )
            self.logger.debug(sql)
            query.execute(sql)
        self.logger.info("Inserted solutions succesfully")
        self.disconnect_db(connection)
