"""-----------------------------"""
"""---- Class to connect DB ----"""
"""-----------------------------"""

import psycopg2
import json
from configuration.logger import Logger
from configuration.database_config import DatabaseConfiguration


class DbManager:
    def __init__(self):
        self.db_conf = DatabaseConfiguration()
        self.config = self.db_conf.db_config
        self.logger = Logger()

    def connect_db(self, password):
        connection = psycopg2.connect(
            host=config.host,
            database=config.name,
            user=config.user,
            password=config.password,
        )
        connection.autocommit = True
        return connection

    def disconnect_db(self, connection):
        connection.close()

    # Get solutions from the db for a excercise id
    def get_solutions(self, exercise_id, password="harryna"):
        connection = self.connect_db(password)
        query = connection.cursor()
        query.execute(
            "SELECT solutions_list FROM solutions WHERE exercise=" + str(exercise_id)
        )
        solution = query.fetchall()
        self.disconnect_db(connection)
        return solution

    # Write the solutions in db
    def post_solutions(self, exercise_data_tuple_list, password):
        connection = self.connect_db(password)
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
