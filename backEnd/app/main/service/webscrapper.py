"""-----------------------------------------------------------------------------"""
"""---- Class to access the web, download exercises and push the correction ----"""
"""-----------------------------------------------------------------------------"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import service.corrector import CorrectorManager

class WebScrapper:

    #Configuration of the explorer 
    chrome_options = webdriver.ChromeOptions()
    DOWNLOAD_PATH = {'download.default_directory' : 'C:\\Users\\User\\Desktop\\CEA\\CORRECTOR_CCC'}
    chrome_options.add_experimental_option('prefs', DOWNLOAD_PATH)
    chrome_options.add_argument('headless')
    DRIVER = webdriver.Chrome(executable_path=r"data/driver/chromedriver.exe", chrome_options=chrome_options)
    TIMEOUT = 3

    #Init url
    URL = "http://www.cursosadistanciayonline.com/index.php"

    def __init__(self):
        pass

    #Open the explorer Chrome
    def initExplorer(self):
        self.self.DRIVER.implicitly_wait(30)
        self.self.DRIVER.maximize_window()
        self.DRIVER.get(self.URL)
        
    def login(self):
        username = self.DRIVER.find_element_by_id("name")
        username.clear()
        username.send_keys("Aitana")

        password = self.DRIVER.find_element_by_name("password")
        password.clear()
        password.send_keys("410")

        self.DRIVER.find_element_by_name("acceder").click()
        self.DRIVER.find_element_by_xpath("//a[@title='CCC']").click()

        print("Logged correctly")

        self.clickExercisesTab()

    #Go to the tab "Ejercicios" from the init page
    def clickExercisesTab(self):
        self.DRIVER.find_element_by_class_name("bejercicio").click()

    #Wait object before click
    def explorer_wait(self, xpath):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present)
        except TimeoutException:
            print("Timeout object ", xpath)

    #If exist more open exercises (has been downloaded)
    def clickOpenExcercises(self, exercise):
        try:
            path = "/html/body/div[3]/div/div[2]/div/div[1]/table/tbody/tr[" + str(exercise) + "]/td[2]/form/input[8]"
            self.explorer_wait(path)
            self.DRIVER.find_element_by_xpath(path).click()
        except NoSuchElementException:
            print("No more exercises to correct")
            return False
        return True

    #Click to download exercise in the download path
    def clickDownload(self):
        try:
            self.explorer_wait(".//a[contains(@href,'cursosccc')]")
            self.DRIVER.find_element_by_xpath(".//a[contains(@href,'cursosccc')]").click()
            self.explorer_wait("/html/body/p[3]/a")
            self.DRIVER.find_element_by_xpath("/html/body/p[3]/a").click()
        except NoSuchElementException:
            print("Error cliking in download")
            return False
        return True

    #Get all exercises in the web
    def numExercises(self):
        tableRows = self.DRIVER.find_element_by_xpath("//table[@id='ejertabla']/tbody").text.split("\n")
        numRows = int(len(tableRows)/2)
        return numRows

    #Download open (has been downloaded) exercises
    def downloadOpenDocs(self):
        numEx = CorrectorManager().numExercises()
        print(numEx, " exercises to download")
        for exercise in  range(1, numEx + 1):
            print("Downloading exercise... " + str(exercise))
            self.clickOpenExcercises(exercise)
            self.clickDownload()
            self.clickExercisesTab()
        print("Exercises download correctly")
        print()
        self.closeExplorer()

    def closeExplorer(self):
        self.DRIVER.quit()

