from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from config.db import collentionlistim
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

url = "https://www.diariolibre.com/tags/violencia-de-genero/528"

path = 'C:/Users/frias/Downloads/chromedriver_win32 (6)/chromedriver.exe'

s = Service(path)

driver = webdriver.Chrome(service=s)


# driver = webdriver.Chrome('C:/Users/frias/Downloads/chromedriver_win32 (6)/chromedriver.exe"')
driver.get(url)
# Hacer clic en el botón "Más Historias" varias veces
for i in range(5):  # hacer clic en el botón tres veces
    try:
        #crear funcion para hacer clic en el boton
        def click_boton():
            boton_mas_historias = driver.find_element(By.XPATH, '/html/body/div[6]/section/div/div/div[2]/div[2]/div[11]/div')
            boton_mas_historias.click()
            time.sleep(8)
        click_boton()
        click_boton()
    except:
        break


soup = BeautifulSoup(driver.page_source, 'html.parser')

items = soup.find_all('article', class_='flex flex-wrap -mx-2 sm:-mx-3')

for item in items:

    title = item.find('h2')
    link = item.find('a', href=True)
    date = item.find('time', datetime=True)['datetime']
    link_diairo = 'https://www.diariolibre.com' + link['href']
    dic = {'Nombre': title.text,'video': link_diairo  ,'fuente':'Diario Libre','fecha': date, 'status': 'Pendiente', 'owner_username': 'Diario Libre'}
    #insertar en la base de datos
    collentionlistim.insert_one(dic)