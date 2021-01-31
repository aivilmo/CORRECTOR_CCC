"""-----------------------------"""
"""---- Class to connect DB ----"""
"""-----------------------------"""

import psycopg2
import json

class DbManager:

    def __init__(self):
        pass

    def connect_db(self, password):
        connection = psycopg2.connect(host="localhost", database="CCC", user="aitana", password=password)
        connection.autocommit = True
        return connection


    def disconnect_db(self, connection):
        connection.close()

    # Get solutions from the db for a excercise id
    def get_solutions(self, exercise_id, password="harryna"):
        connection = self.connect_db(password)
        query = connection.cursor()
        query.execute("SELECT solutions_list FROM solutions WHERE exercise=" + str(exercise_id))
        solution = query.fetchall()
        self.disconnect_db(connection)
        return solution

    # Write the solutions in db
    def post_solutions(self, exercise_data_tuple_list, password):
        connection = self.connect_db(password)
        print("Inserting solutions in db...")
        query = connection.cursor()
        filename_list = []
        for tuple_item in exercise_data_tuple_list:
            filename, number_of_exercise, response, num_questions = tuple_item
            filename_list.append(filename)
            args = (num_questions, number_of_exercise, json.dumps(response))
            sql = "INSERT INTO public.solutions(num_questions, exercise, solutions_list) VALUES {} ON CONFLICT (exercise) DO NOTHING ".format(
                args
            )
            # print(sql)
            query.execute(sql)
        print("Inserted solutions succesfully")
        self.disconnect_db(connection)
