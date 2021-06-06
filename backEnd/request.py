import requests
from bs4 import BeautifulSoup
import re

# URL que entrega las cookies
INIT_URL = "http://www.cursosadistanciayonline.com/"

# login
LOGIN_URL = "http://www.cursosadistanciayonline.com/acceso.php"

# Esta preprocesa la siguiente url por alguna razon
GESTION = "http://www.cursosadistanciayonline.com/gestionp.php?id=0"

# tabla de ejercicios, fijate que esta tu contraseña en la URL
EXERCISE_TABLE = "http://www.cursosadistanciayonline.com/lista_ejercicios_pendientes1.php?clave=410&empresa=0"

# pagina para la descarga del doc
DOWNLOAD_PAGE = (
    "http://www.cursosadistanciayonline.com/predescargar_ejercicio_seleccionado1.php"
)

# se obtienen las cookies
index = requests.get(INIT_URL)
req_cookies = index.cookies


# se logea
login = requests.post(
    LOGIN_URL,
    headers={
        "Origin": "http://www.cursosadistanciayonline.com",
        "Referer": "http://www.cursosadistanciayonline.com/index.php",
    },
    cookies=req_cookies,
    data={"usuario": "Aitana", "password": "410", "acceder": "Acceder"},
)

# preformateo
gestion = requests.get(GESTION, cookies=req_cookies)


# obtiene las tablas y pasa el HTML obtenido
tables = requests.get(EXERCISE_TABLE, cookies=req_cookies)
soup = BeautifulSoup(tables.text, "html.parser")

# busca todas las filas
rows = soup.find_all("tr")

# Se iteran todas las filas buscando preformatear el body de las request
# primero busca un form especifico ya que dentro de las tr hay varios form
# luego busco los datos para el body
# si encuentra la class submit quiere decir que es la primera vez que se abrio el enlace
# si encuentra la class boton quiere decir que ya fue abierto
requestsBodies = []
for i in range(1, len(rows)):
    form = rows[i].find(
        "form",
        {
            "action": "http://www.cursosadistanciayonline.com/predescargar_ejercicio_seleccionado1.php"
        },
    )
    body = {
        "num_interesado": form.find("input", {"name": "num_interesado"})["value"],
        "num_matricula": form.find("input", {"name": "num_matricula"})["value"],
        "num_anexo": form.find("input", {"name": "num_anexo"})["value"],
        "num_curso": form.find("input", {"name": "num_curso"})["value"],
        "num_ejercicio": form.find("input", {"name": "num_ejercicio"})["value"],
        "num_repeticion": form.find("input", {"name": "num_repeticion"})["value"],
        "enviar": "Descargar",
    }

    if form.find("input", {"name": "enviar", "class": "submit"}):
        body["cod_profe"] = "410"
    elif form.find("input", {"name": "enviar", "class": "boton"}):
        body["segunda"] = "S"
    requestsBodies.append(body)

# con los bodies preparados itera adjuntando a cada uno al request para abrir las paginas de descargas
# busca el enlace de descarga de las pags
# descarga
# extrae el nombre del fichero
# ya que no se permite la descarga directa de ficheros, escribe el fichero
for body in requestsBodies:

    downloadResp = requests.post(DOWNLOAD_PAGE, cookies=req_cookies, data=body)
    soup = BeautifulSoup(downloadResp.text, "html.parser")
    link = soup.find("a")["href"]
    docx = requests.get(link, allow_redirects=True, stream=True)
    pattern = "http://campus.cursosccc.com//wordalum/(.*)"
    match = re.search(pattern, link)
    if match:
        doc_name = match.group(1)

    with open(doc_name, "wb") as f:
        for chunk in docx.iter_content(1024 * 1024 * 2):  # 2 MB chunks
            f.write(chunk)
