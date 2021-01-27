"""-----------------------------"""
"""---- Class to connect DB ----"""
"""-----------------------------"""

import psycopg2
import json
from .corrector import *

def connect_db(password):
    connection = psycopg2.connect(host="localhost", database="CCC", user="aitana", password=password)
    connection.autocommit = True
    return connection

def disconnect_db(connection):
    connection.close()

# Get solutions from the db for a excercise id
def get_solutions(exercise_id, password="harryna"):
    connection = connect_db(password)
    query = connection.cursor()
    query.execute("SELECT solutions_list FROM solutions WHERE exercise=" + str(exercise_id))
    solution = query.fetchall()
    disconnect_db(connection)
    return solution

# Write the solutions in db
def post_solutions(solutions_list, password):
    connection = connect_db(password)
    print("Inserting solutions in db...")
    query = connection.cursor()
    for solution_file in solutions_list:
        response, num_questions = extract_solution_docx(solution_file)
        args = (num_questions, number_exercise(solution_file), json.dumps(response))
        sql = "INSERT INTO public.solutions(num_questions, exercise, solutions_list) VALUES {} ON CONFLICT (exercise) DO NOTHING ".format \
            (args)
        # print(sql)
        query.execute(sql)
    print("Inserted solutions succesfully")
    disconnect_db(connection)
