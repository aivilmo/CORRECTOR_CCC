"""-----------------------------------------------------------------------------"""
"""---- Class to access the web, download exercises and push the correction ----"""
"""-----------------------------------------------------------------------------"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from definitions import BASE_FOLDER

# Configuration of the explorer

chrome_options = webdriver.ChromeOptions()
print(str(BASE_FOLDER.absolute()) + "\\data\\storage\\exercises\\")
DOWNLOAD_PATH = {
    "download.default_directory": str(BASE_FOLDER.absolute())
    + "\\data\\storage\\exercises\\"
}
chrome_options.add_experimental_option("prefs", DOWNLOAD_PATH)
chrome_options.add_argument("headless")
DRIVER = webdriver.Chrome(
    executable_path=r"data/driver/chromedriver.exe", chrome_options=chrome_options
)
TIMEOUT = 3

# Init url
URL = "http://www.cursosadistanciayonline.com/index.php"

# Open the explorer Chrome
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

    clickExercisesTab()


# Go to the tab "Ejercicios" from the init page
def clickExercisesTab():
    DRIVER.find_element_by_class_name("bejercicio").click()


# Wait object before click
def explorer_wait(xpath):
    try:
        print("Waiting ...")
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(DRIVER, TIMEOUT).until(element_present)
    except TimeoutException:
        print("Timeout object ", xpath)


# If exist more open exercises (has been downloaded)
def clickOpenExcercises(exercise):
    try:
        path = (
            "/html/body/div[3]/div/div[2]/div/div[1]/table/tbody/tr["
            + str(exercise)
            + "]/td[2]/form/input[8]"
        )
        explorer_wait(path)
        DRIVER.find_element_by_xpath(path).click()
    except NoSuchElementException:
        print("No more exercises to correct")
        return False
    return True


# Click to download exercise in the download path
def clickDownload():
    try:
        explorer_wait(".//a[contains(@href,'cursosccc')]")
        DRIVER.find_element_by_xpath(".//a[contains(@href,'cursosccc')]").click()
        explorer_wait("/html/body/p[3]/a")
        DRIVER.find_element_by_xpath("/html/body/p[3]/a").click()
    except NoSuchElementException:
        print("Error cliking in download")
        return False
    return True


# Get all exercises in the web
def numExercises():
    tableRows = DRIVER.find_element_by_xpath(
        "//table[@id='ejertabla']/tbody"
    ).text.split("\n")
    numRows = int(len(tableRows) / 2)
    return numRows


# Download open (has been downloaded) exercises
def downloadOpenDocs():
    numEx = numExercises()
    print(numEx, " exercises to download")
    for exercise in range(1, numEx + 1):
        print("Downloading exercise... " + str(exercise))
        clickOpenExcercises(exercise)
        clickDownload()
        clickExercisesTab()
    print("Exercises download correctly")
    print()
    closeExplorer()


def closeExplorer():
    DRIVER.quit()
