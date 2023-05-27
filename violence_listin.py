from datetime import datetime
import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from dateutil import parser
import locale
from config.db import collectionportal,


locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

url = "https://www.diariolibre.com/tags/violencia-de-genero/528"

path = 'chromedriver.exe'

s = Service(path)
driver = webdriver.Chrome(service=s)
# chrome_options.add_argument('--headless'
chrome_options = Options()
chrome_options.add_argument('--headless')
# driver = webdriver.Chrome('C:/Users/frias/Downloads/chromedriver_win32 (6)/chromedriver.exe"')
driver.get(url)
# Hacer clic en el botón "Más Historias" varias veces
for i in range(5):  # hacer clic en el botón tres veces
    try:
        #crear funcion para hacer clic en el boton
        def click_boton():
            boton_mas_historias = driver.find_element(By.XPATH, '/html/body/div[6]/section/div/div/div[2]/div[2]/div[11]/div')
            boton_mas_historias.click()
            time.sleep(12)
        click_boton()
        click_boton()
    except:
        break

#crear una funcion para el mes la fecha y el año


soup = BeautifulSoup(driver.page_source, 'html.parser')

items = soup.find_all('article', class_='flex flex-wrap -mx-2 sm:-mx-3')

for item in items:

    title = item.find('h2')
    link = item.find('a', href=True)
    date = item.find('time',title=True)
    date1 = date['title']
    img = item.find('img', src=True)

    #obtner tmabien las imagenes despues del boton mas historias
    if img is not None:
        imagen = img['src']
    else:
        #poner las demas imagenes en un else
        # imagen = img['src']
        current_source = item.find('source', srcset=True)
        #unshif para agregar al inicio de la lista
        imagen = 'https://www.diariolibre.com' + current_source['srcset'].split(',')[0].strip()


        
    date = datetime.datetime.strptime(date1, '%B %d, %Y')
    date_formatted = date.strftime('%d-%m-%Y')
    #bajar solo las noticias de ayer y hoy
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%d-%m-%Y')
    today = datetime.datetime.now()
    today = today.strftime('%d-%m-%Y')
    if date_formatted == yesterday or date_formatted == today:
        print('es de hoy o ayer')
    else:
        continue

 

    link_diairo = 'https://www.diariolibre.com' + link['href']
     
    dic = {'Titulo': title.text,'video': link_diairo  ,'fuente':'Diario Libre', 'fecha': date_formatted, 'imagen': imagen,'status': 'Pendiente',"name": "Diario Libre", "Lastname": "Diario Libre", "longitude": -69.9000000, "latitude": 18.4833333, "clasificacion": "Violencia de Genero", "descripcion": "Violencia de Genero"}
    print(dic)
    try:
        collectionportal.insert_one(dic)
    except BaseException as e:
            print('Status Failed On,', str(dic), 'With Error', str(e))
            

