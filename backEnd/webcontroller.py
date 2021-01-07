

"""-----------------------------------------------------------------------------"""
"""---- Class to access the web, download exercises and push the correction ----"""
"""-----------------------------------------------------------------------------"""

from lib import *

#Configuration of the explorer 
chrome_options = webdriver.ChromeOptions()
DOWNLOAD_PATH = {'download.default_directory' : 'C:\\Users\\User\\Desktop\\CEA\\CORRECTOR_CCC'}
chrome_options.add_experimental_option('prefs', DOWNLOAD_PATH)
chrome_options.add_argument('headless')
DRIVER = webdriver.Chrome(chrome_options=chrome_options)

#Init url
URL = "http://www.cursosadistanciayonline.com/index.php"

#Open the explorer Chrome
def initExplorer():
    DRIVER.implicitly_wait(30)
    DRIVER.maximize_window()
    DRIVER.get(URL)
    

def login():
    username = DRIVER.find_element_by_id("name")
    username.clear()
    username.send_keys("Aitana")

    password = DRIVER.find_element_by_name("password")
    password.clear()
    password.send_keys("410")

    DRIVER.find_element_by_name("acceder").click()
    DRIVER.find_element_by_xpath("//a[@title='CCC']").click()

    print("Logged correctly")

    exercisesTab()

#Go to the tab "Ejercicios" from the init page
def exercisesTab():
    DRIVER.find_element_by_class_name("bejercicio").click()

#If exist more pending exercises (not downloaded yet)
def existPendingExcercises():
    try:
        DRIVER.find_element_by_class_name("submit").click()
    except NoSuchElementException:
        print("No hay mas ejercicos pendientes para corregir")
        return False
    return True

#If exist more open exercises (has been downloaded)
def existOpenExcercises(row):
    try:
        DRIVER.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div[1]/table/tbody/tr[" + \
        str(row) + "]/td[2]/form/input[8]").click()
    except NoSuchElementException:
        print("No hay mas ejercicos abiertos para corregir")
        return False
    return True

#Click to download exercise in the download path
def clickDownload():
    DRIVER.find_element_by_xpath("/html/body/p[1]/a").click()
    #print("click /html/body/p[1]/a")
    DRIVER.find_element_by_xpath("/html/body/p[3]/a").click()

#Get all exercises in the web
def numExercises():
    tableRows = DRIVER.find_element_by_xpath("//table[@id='ejertabla']/tbody").text.split("\n")
    numRows = int(len(tableRows)/2)
    return numRows

#Download pending (not downloaded yet) exercises
def downloadPendingDocs():
    while existPendingExcercises():
        print("Descargando ejercicio pendiente...")
        clickDownload()
        exercisesTab()
    return

#Download open (has been downloaded) exercises
def downloadOpenDocs():
    row = 1
    while existOpenExcercises(row):
        print("Descargando ejercicio abierto... " + str(row))
        clickDownload()
        exercisesTab()
        row += 1
    return

#Download all docs avaliables 
def downloadAllDocs():
    downloadOpenDocs()
    downloadPendingDocs()

