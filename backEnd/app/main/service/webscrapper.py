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
from configuration.logger import Logger
import time


class WebScrapper:

    # Configuration of the explorer
    chrome_options = webdriver.ChromeOptions()
    DOWNLOAD_PATH = {
        "download.default_directory": str(BASE_FOLDER.absolute())
        + "\\data\\storage\\exercises\\"
    }
    chrome_options.add_experimental_option("prefs", DOWNLOAD_PATH)
    # chrome_options.add_argument("headless")
    DRIVER = webdriver.Chrome(
        executable_path=r"data/driver/chromedriver.exe", chrome_options=chrome_options
    )
    TIMEOUT = 3

    # Init url
    URL = "http://www.cursosadistanciayonline.com/index.php"

    def __init__(self):
        self.logger = Logger()

    # Open the explorer Chrome
    def init_explorer(self):
        self.DRIVER.implicitly_wait(30)
        self.DRIVER.maximize_window()
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

        self.logger.info("Logged correctly")

        self.click_exercises_tab()

    # Go to the tab "Ejercicios" from the init page
    def click_exercises_tab(self):
        self.DRIVER.find_element_by_class_name("bejercicio").click()
        self.wait_table_content_be_loaded()

    # Wait object before click
    def explorer_wait(self, xpath):
        try:
            self.logger.info("Waiting ...")
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present)
        except TimeoutException:
            self.logger.error("Timeout object " + xpath)

    # If exist more open exercises (has been downloaded)
    def click_open_excercises(self, exercise):
        try:
            path = (
                "/html/body/div[3]/div/div[2]/div/div[1]/table/tbody/tr["
                + str(exercise)
                + "]/td[2]/form/input[8]"
            )
            self.explorer_wait(path)
            self.DRIVER.find_element_by_xpath(path).click()
        except NoSuchElementException:
            self.logger.error("No more exercises to correct")
            return False
        return True

    # Click to download exercise in the download path
    def click_download(self):
        try:
            self.explorer_wait(".//a[contains(@href,'cursosccc')]")
            self.DRIVER.find_element_by_xpath(
                ".//a[contains(@href,'cursosccc')]"
            ).click()
            self.explorer_wait("/html/body/p[3]/a")
            self.DRIVER.find_element_by_xpath("/html/body/p[3]/a").click()
        except NoSuchElementException:
            self.logger.error("Error cliking in download")
            return False
        return True

    # Get all exercises in the web
    def num_exercises(self):
        self.wait_table_content_be_loaded()
        tableRows = self.DRIVER.find_element_by_xpath(
            "//table[@id='ejertabla']/tbody"
        ).text.split("\n")
        numRows = int(len(tableRows) / 2)
        if self.DRIVER.find_element_by_class_name("dataTables_empty"):
            self.DRIVER.quit()
            raise Exception("No exercises to download")
        return numRows

    def wait_table_content_be_loaded():
        element_present = EC.presence_of_element_located(
            (By.XPATH, "//table[@id='ejertabla']/tbody")
        )
        WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present)

    # Download open (has been downloaded) exercises
    def download_docs(self):
        numEx = self.num_exercises()
        self.logger.info(str(numEx) + " exercises to download")
        for exercise in range(1, numEx + 1):
            self.logger.info("Downloading exercise... " + str(exercise))
            self.click_open_excercises(exercise)
            self.click_download()
            self.click_exercises_tab()
        self.logger.info("Exercises download correctly")
        self.close_explorer()

    def close_explorer(self):
        self.DRIVER.quit()
