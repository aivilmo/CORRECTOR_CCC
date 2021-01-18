"""--------------------------------------------------"""
"""---- Import Class to add all libraries needed ----"""
"""--------------------------------------------------"""

import requests 
import docx
import re
import win32com.client
import glob
import os
import sys
import io
import json
import psycopg2 

from bs4 import BeautifulSoup
from docx.shared import RGBColor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bdconnection import *
from webcontroller import *
from corrector import *