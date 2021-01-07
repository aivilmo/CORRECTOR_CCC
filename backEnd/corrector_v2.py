"""----------------------------------"""
"""---- Main and Corrector Class ----"""
"""----------------------------------"""

from lib import *

#Const
EXTENSION_LIST = ["doc", "docx", "odt", "pdf"]
IGNORED_EXERCISES = [7, 8, 9, 12, 13] #Nat = 7, 8, 9 | FB = 12, 13
INDEX_CALIFICATION = 10
INDEX_COMMENTARY = 11


def numberExercise(fileName):
    return int(fileName.split("_Ejercicio_")[1].split("_")[0])

#Convert doc to docx
def doc2docx(isSolution = False):
    Word = win32com.client.Dispatch("Word.Application")
    Word.visible = 0
    path = "..\*."
    if (isSolution):
        path = "Soluciones\*." 
    for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[0])):
        in_file = os.path.abspath(doc)
        wb = Word.Documents.Open(in_file)
        out_file = os.path.abspath(in_file[:-4]+ "." + EXTENSION_LIST[1])
        print("Converting " + in_file + " to " + out_file + "...")
        print("")
        wb.SaveAs2(out_file, FileFormat=16) # file format for docx
        wb.Close()
        os.remove(in_file)

    Word.Quit()

#Extract response from the docx
def cleanResponse(response, isSolution):
    responses = re.findall("[a-v]", response)
    if (not isSolution):
        return responses
    else:
        return responses[:-4]

#Read responses and correct the docx
def correctExerciseDocx(filename):
    num_exercise = numberExercise(filename)
    if(num_exercise in IGNORED_EXERCISES):
            print("Ignoring " + filename)
            return
    try:
        document = docx.Document(filename)
        responses = dict()
        question = 1
        wrongAnswer = 0
        solution = getSolutions(num_exercise)
        if (solution == []):
            print("No solution in DB to ejercise " + str(num_exercise))
            return
        solution = solution[0][0]
        solution_keys = list(solution.keys())
        for paragraph in document.paragraphs:
            paragraph_text = paragraph.text
            index = paragraph_text.find("La respuesta es")
            if (index != -1):
                response = paragraph_text.split(":")
                responses[question] = cleanResponse(response[1].lower(), False)
                solution_key = solution_keys[question-1]
                if (set(responses[question]) != set(solution[solution_key])):
                    wrongAnswer += 1
                    correction = paragraph.add_run(solution[solution_key])
                else:
                    correction = paragraph.add_run("bien")
                setStyle(correction)
                question += 1
        if (question == 1):
            print("Error reading responses " + filename)
            return
        question -= 1
        grade = round(((question - wrongAnswer) * 10) / question, 2)
        print(filename)
        print("Grade: " + str(grade))
        print("")
        grade_str = document.paragraphs[INDEX_CALIFICATION].add_run(str(grade))
        commentary = generateCommentary(grade)
        commentary_str = document.paragraphs[INDEX_COMMENTARY].add_run(commentary)
        setStyle(grade_str)
        setStyle(commentary_str)
    except Exception as e:
        print("Error in file " + filename)
        print(str(e))
    document.save(filename[:-5]+"_CORREGIDO.docx")
    os.remove(filename)
    return responses, question - 1 

#Set read letters to correct the docx
def setStyle(paragraph):
    paragraph.bold = True
    paragraph.font.color.rgb = RGBColor(255,0,0)

#Generate commentary from the docx
def generateCommentary(grade):
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

#Extract response from the solution docx
def extractSolutionDocx(filename):
    num_exercise = numberExercise(filename)
    try:
        document = docx.Document(filename)
        responses = dict()
        question = 1
        for paragraph in document.paragraphs:
            paragraph_text = paragraph.text
            index = paragraph_text.find("La respuesta es")
            if (index != -1):
                response = paragraph_text.split(":")
                responses[question] = cleanResponse(response[1].lower(), True)
                question += 1
    except Exception as e:
        print("Error in file " + filename)
        print(str(e))
    return responses, question - 1 

#Get the list of the exercises downloaded
def readFiles(isSolution = False):
    solutions_list = []
    path = "..\*."
    if (isSolution):
        path = "Soluciones\*."
    for i, doc in enumerate(glob.iglob(path + EXTENSION_LIST[1])):
        in_file = os.path.abspath(doc)
        solutions_list.append(in_file)
    return solutions_list

#Correct all exercises in the path
def correct():
    doc2docx()
    print("Correcting exercises...")
    print("")
    for doc in readFiles():
        correctExerciseDocx(doc)

#Main
if __name__ == "__main__":
    """----------------------------"""
    """----to correct exercises----"""
    """----------------------------"""
    initExplorer()
    login()
    downloadOpenDocs()
    correct()
    """----------------------------------"""
    """----to pass the solutions to DB----"""
    """----------------------------------"""
    """
    doc2docx(True)
    solutions = readFiles(True)
    postSolutions(solutions, password="harryna")
    """