from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import requests
import traceback
import logging
from time import sleep
import datetime
import os
import json

data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{data_atual}.log', mode='a'),
        logging.StreamHandler()  # Adiciona saída para o console
    ]
)

class Webmotors:

    def process_link(self, link):
        try:                
            data_for_telegram = self.get_cars(link)
            try: self.driver.quit()
            except: pass
            return data_for_telegram
        
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception(f"Erro ao abrir site {error}")
        
    def get_cars(self, link):
        try:
            logging.info('Procurando carros ---')
            url = f'https://www.webmotors.com.br/api/search/car?url={link}&actualPage=1&displayPerPage=70'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.webmotors.com.br/',
                'Connection': 'keep-alive'
            }
            session = requests.Session()
            session.headers.update(headers)
            response = requests.get(url, headers=headers)

            cars_data = json.loads(response.text)

            data_for_telegram = []
            
            with open("links/linksWebmotors.txt", "r", encoding="utf-8") as file:
                links_existentes = file.read().splitlines()

            for car in cars_data.get('SearchResults', []):
                title = car['Specification']['Title']
                price = car['Prices']['Price']
                href = f"https://www.webmotors.com.br/comprar/{car['Specification']['Make']['Value']}/{car['Specification']['Model']['Value']}/{car['UniqueId']}"
                km = f"{car['Specification']['Odometer']} km"
                year = f"{car['Specification']['YearFabrication']}/{car['Specification']['YearModel']}"

                title_formatted = f'{title}'
                value_formatted = f'R$ {price:,.2f}'.replace(",", ".").replace(".", ",", 1)

                if href not in links_existentes:
                    with open("links/linksWebmotors.txt", "a", encoding="utf-8") as file:
                        file.write(href + "\n")
                    data_car = [title_formatted, value_formatted, href, km, year]
                    data_for_telegram.append(data_car)
            return data_for_telegram
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar carros: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            self.driver.quit()
            raise Exception('Erro ao encontrar carros')
