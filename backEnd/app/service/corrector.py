"""---------------------------"""
"""----- Corrector Class -----"""
"""---------------------------"""

from configuration.lib import *

# Const
EXTENSION_LIST = ["doc", "docx", "odt", "pdf"]
IGNORED_EXERCISES = [7, 8, 9, 12, 13]  # Nat = 7, 8, 9 | FB = 12, 13
INDEX_CALIFICATION = 10
INDEX_COMMENTARY = 11


def number_exercise(file_name):
    return int(file_name.split("_Ejercicio_")[1].split("_")[0])


# Convert doc to docx
def doc2docx(is_solution=False):
    Word = win32com.client.Dispatch("Word.Application")
    Word.visible = 0
    path = "..\*."
    if (is_solution):
        path = "Soluciones\*."
    for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[0])):
        in_file = os.path.abspath(doc)
        wb = Word.Documents.Open(in_file)
        out_file = os.path.abspath(in_file[:-4] + "." + EXTENSION_LIST[1])
        print("Converting " + in_file + " to " + out_file + "...")
        print("")
        wb.SaveAs2(out_file, FileFormat=16)  # file format for docx
        wb.Close()
        os.remove(in_file)

    Word.Quit()

# Extract response from the docx
def clean_response(response, is_solution):
    responses = re.findall("[a-v]", response)
    if (not is_solution):
        return responses
    else:
        return responses[:-4]

# Read responses and correct the docx
def correct_exercise_docx(filename):
    num_exercise = number_exercise(filename)
    if (num_exercise in IGNORED_EXERCISES):
        print("Ignoring " + filename)
        return
    try:
        document = docx.Document(filename)
        responses = dict()
        question = 1
        wrong_answer = 0
        solution = get_solutions(num_exercise)
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
                responses[question] = clean_response(response[1].lower(), False)
                solution_key = solution_keys[question - 1]
                if (set(responses[question]) != set(solution[solution_key])):
                    wrong_answer += 1
                    correction = paragraph.add_run(solution[solution_key])
                else:
                    correction = paragraph.add_run(" bien")
                set_style(correction)
                question += 1
        if (question == 1):
            print("Error reading responses " + filename)
            return
        question -= 1
        grade = round(((question - wrong_answer) * 10) / question, 2)
        print(filename)
        print("Grade: " + str(grade))
        print("")
        grade_str = document.paragraphs[INDEX_CALIFICATION].add_run(str(grade))
        commentary = generate_commentary(grade)
        commentary_str = document.paragraphs[INDEX_COMMENTARY].add_run(commentary)
        set_style(grade_str)
        set_style(commentary_str)
    except Exception as e:
        print("Error in file " + filename)
        print(str(e))
    document.save(filename[:-5] + "_CORREGIDO.docx")
    os.remove(filename)
    return responses, question - 1

# Set read letters to correct the docx
def set_style(paragraph):
    paragraph.bold = True
    paragraph.font.color.rgb = RGBColor(255, 0, 0)

# Generate commentary from the docx
def generate_commentary(grade):
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
def extract_solution_docx(filename):
    num_exercise = number_exercise(filename)
    try:
        document = docx.Document(filename)
        responses = dict()
        question = 1
        for paragraph in document.paragraphs:
            paragraph_text = paragraph.text
            index = paragraph_text.find("La respuesta es")
            if (index == -1):
                index = paragraph_text.find("La respuesta correcta es")
            if (index != -1):
                response = paragraph_text.split(":")
                responses[question] = clean_response(response[1].lower(), True)
                question += 1
    except Exception as e:
        print("Error in file " + filename)
        print(str(e))
    return responses, question - 1

# Get the list of the exercises downloaded
def read_files(isSolution=False):
    solutions_list = []
    path = "..\*."
    if (isSolution):
        path = "..\..\EJERCICIOS_CCC\Soluciones\*."
    for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[1])):
        in_file = os.path.abspath(doc)
        solutions_list.append(in_file)
    return solutions_list

# Correct all exercises in the path
def correct():
    doc2docx()
    print("Correcting exercises...")
    print("")
    for doc in read_files():
        correct_exercise_docx(doc)
