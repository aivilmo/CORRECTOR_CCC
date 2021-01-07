

"""-----------------------------"""
"""---- Class to connect DB ----"""
"""-----------------------------"""

from lib import *

def connectDB(passwrd):
    connection = psycopg2.connect(host="localhost", database="CCC", user="aitana", password=passwrd)
    connection.autocommit = True
    return connection


def disconnectDB(connection):
    connection.close()

#Get solutions from the db for a excercise id
def getSolutions(exercise_id, password="harryna"):
    connection = connectDB(password)
    query = connection.cursor()
    query.execute("SELECT solutions_list FROM solutions WHERE exercise=" + str(exercise_id))
    solution = query.fetchall()
    disconnectDB(connection)
    return solution

#Write the solutions in db
def postSolutions(solutions_list, password):
    connection = connectDB(password)
    query = connection.cursor()
    for solution_file in solutions_list:
        response, num_questions  = correctSolutionDocx(solution_file)
        args =  (num_questions, numberExercise(solution_file), json.dumps(response))
        sql = "INSERT INTO public.solutions(num_questions, exercise, solutions_list) VALUES {} ON CONFLICT (exercise) DO NOTHING ".format(args)
        #print(sql)
        query.execute(sql)
    disconnectDB(connection)
