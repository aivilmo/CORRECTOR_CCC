import requests
from bs4 import BeautifulSoup
import re
from configuration.logger import Logger
from configuration.app_config_v2 import AppConfig


class FileDownloader:

    BASE_URL = "http://www.cursosadistanciayonline.com/"
    # login
    LOGIN = "acceso.php"
    # This site preprocess all other PHP calls
    GESTION = "gestionp.php?id=0"
    # Site to download specific exercise
    DOWNLOAD_PAGE = "predescargar_ejercicio_seleccionado1.php"

    def __init__(self):
        self.logger = Logger()
        self.req_cookies = []
        self.requestsBodies = []
        self.app_config = AppConfig()
        # The exercise table
        self.EXERCISE_TABLE = "lista_ejercicios_pendientes1.php?clave=" + str(self.app_config.ccc_password()) + "&empresa=0"

    def _get_session_tokens(self):
        index = requests.get(self.BASE_URL)
        self.req_cookies = index.cookies
        if len(self.req_cookies) > 0:
            self.logger.info("Sessions and cookies were obtained")
        else:
            self.logger.error("Could not get sessions")

    def _login(self):
        self.logger.info("Signing in to CCC...")
        requests.post(
            self.BASE_URL + self.LOGIN,
            headers={
                "Origin": self.BASE_URL,
                "Referer": self.BASE_URL + "index.php",
            },
            cookies=self.req_cookies,
            data={"usuario": self.app_config.ccc_username(), "password": self.app_config.ccc_password(), "acceder": "Acceder"},
        )

        preformat = self._preformat_php()

        if not "¡Hola  -! " in preformat.text:
            self.logger.info("Sign in to CCC correct")
        else:
            self.logger.error("Could not log in to CCC")

    def _preformat_php(self):
        return requests.get(self.BASE_URL + self.GESTION, cookies=self.req_cookies)

    def _get_exercises(self):
        tables = requests.get(
            self.BASE_URL + self.EXERCISE_TABLE, cookies=self.req_cookies
        )
        soup = BeautifulSoup(tables.text, "html.parser")

        # find all rows
        rows = soup.find_all("tr")

        if len(rows) > 1:
            self.logger.info("Found exercises to download")
        else:
            self.logger.info("There are no exercises to download")
            return False

        self.requestsBodies = []
        for i in range(1, len(rows)):
            form = rows[i].find("form", {"action": self.BASE_URL + self.DOWNLOAD_PAGE})
            body = {
                "num_interesado": self._find_input_value(form, "num_interesado"),
                "num_matricula": self._find_input_value(form, "num_matricula"),
                "num_anexo": self._find_input_value(form, "num_anexo"),
                "num_curso": self._find_input_value(form, "num_curso"),
                "num_ejercicio": self._find_input_value(form, "num_ejercicio"),
                "num_repeticion": self._find_input_value(form, "num_repeticion"),
                "enviar": "Descargar",
            }

            # This may work when automated file upload exist
            if form.find("input", {"name": "enviar", "class": "submit"}):
                body["cod_profe"] = self.app_config.ccc_password()
            elif form.find("input", {"name": "enviar", "class": "boton"}):
                body["segunda"] = "S"
            self.requestsBodies.append(body)
            return True

    def _find_input_value(self, form, field):
        return form.find("input", {"name": field})["value"]

    def _download_exercises_from_ccc(self):
        self.logger.info("Downloading exercises...")
        for body in self.requestsBodies:
            self.logger.info("Downloading exercise...")
            downloadResp = requests.post(
                self.BASE_URL + self.DOWNLOAD_PAGE, cookies=self.req_cookies, data=body
            )
            soup = BeautifulSoup(downloadResp.text, "html.parser")
            link = soup.find("a")["href"]
            docx = requests.get(link, allow_redirects=True, stream=True)
            pattern = "http://campus.cursosccc.com//wordalum/(.*)"

            # Exercise name
            match = re.search(pattern, link)
            if match:
                doc_name = "data/storage/exercises/" + match.group(1)

            with open(doc_name, "wb") as f:
                for chunk in docx.iter_content(1024 * 1024 * 2):  # 2 MB chunks
                    f.write(chunk)
                self.logger.info("Exercise downloaded: " + match.group(1))

    def download_exercises(self):
        self._get_session_tokens()
        self._login()
        if self._get_exercises():
            self._download_exercises_from_ccc()
            return True
        return False
