import requests
from bs4 import BeautifulSoup
import re


class FileDownloader:

    BASE_URL = "http://www.cursosadistanciayonline.com/"

    # login
    LOGIN = "acceso.php"
    # This site preprocess all other PHP calls
    GESTION = "gestionp.php?id=0"
    # The exercise table
    EXERCISE_TABLE = "lista_ejercicios_pendientes1.php?clave=410&empresa=0"
    # Site to download specific exercise
    DOWNLOAD_PAGE = "predescargar_ejercicio_seleccionado1.php"

    def __init__(self):
        self.req_cookies = []
        self.requestsBodies = []

    def _get_session_tokens(self):
        index = requests.get(self.BASE_URL)
        self.req_cookies = index.cookies

    def _login(self):
        requests.post(
            self.BASE_URL + self.LOGIN,
            headers={
                "Origin": "http://www.cursosadistanciayonline.com",
                "Referer": "http://www.cursosadistanciayonline.com/index.php",
            },
            cookies=self.req_cookies,
            data={"usuario": "Aitana", "password": "410", "acceder": "Acceder"},
        )

    def _preformat_php(self):
        requests.get(self.BASE_URL + self.GESTION, cookies=self.req_cookies)

    def _get_exercises(self):
        tables = requests.get(
            self.BASE_URL + self.EXERCISE_TABLE, cookies=self.req_cookies
        )
        soup = BeautifulSoup(tables.text, "html.parser")

        # find all rows
        rows = soup.find_all("tr")

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

            """
            #This may work when automated file upload exist
            if form.find("input", {"name": "enviar", "class": "submit"}):
                body["cod_profe"] = "410"
            elif form.find("input", {"name": "enviar", "class": "boton"}):"""
            body["segunda"] = "S"
            self.requestsBodies.append(body)

    def _find_input_value(self, form, field):
        return form.find("input", {"name": field})["value"]

    def _download_exercises_from_ccc(self):
        for body in self.requestsBodies:

            downloadResp = requests.post(
                self.BASE_URL + self.DOWNLOAD_PAGE, cookies=self.req_cookies, data=body
            )
            soup = BeautifulSoup(downloadResp.text, "html.parser")
            link = soup.find("a")["href"]
            docx = requests.get(link, allow_redirects=True, stream=True)
            pattern = "http://campus.cursosccc.com//wordalum/(.*)"
            match = re.search(pattern, link)
            if match:
                doc_name = "data/storage/exercises" + match.group(1)

            with open(doc_name, "wb") as f:
                for chunk in docx.iter_content(1024 * 1024 * 2):  # 2 MB chunks
                    f.write(chunk)

    def download_exercises(self):
        self._get_session_tokens()
        self._login()
        self._preformat_php()
        self._get_exercises()
        self._download_exercises_from_ccc()
