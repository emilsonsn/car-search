from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver
import traceback
import logging
from time import sleep
import datetime
import os
import subprocess
import platform
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
            system = platform.system()

            options = [
                '--no-sandbox',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-infobars',
                '--log-level=3',
                '--remote-debugging-port=9222',
            ]            

            options = " ".join(options)
            
            if system == "Windows":
                subprocess.Popen(
                    f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" {options}', shell=True)
            elif system == "Linux":
                subprocess.Popen(
                    f'/usr/bin/google-chrome {options}', shell=True)
            
            sleep(1)
            service = Service()
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")         

            if system == "Windows":
                self.driver = webdriver.Chrome(service=service, options=self.options)
            elif system == "Linux":
                self.driver = webdriver.Chrome(service=service, options=self.options)
            
            url = f'https://www.webmotors.com.br/api/search/car?url={link}&actualPage=1&displayPerPage=1000'
            self.driver.get(url)

            data_json = json.loads(self.driver.find_element(By.CSS_SELECTOR, 'pre').text)
            self.driver.quit()
            sleep(5)
            data_for_telegram = self.get_cars(data_json)
            try: self.driver.quit()
            except: pass
            return data_for_telegram
        
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception(f"Erro ao abrir site {error}")
        
    def get_cars(self, cars_data):
        try:
            logging.info('Procurando carros ---')

            data_for_telegram = []
            
            with open("links/linksWebmotors.txt", "r", encoding="utf-8") as file:
                links_existentes = {line.strip() for line in file if line.strip()}

            for car in cars_data.get('SearchResults', []):
                title = car['Specification']['Title']
                price = car['Prices']['Price']
                href = self.buildUrl(car)
                km = f"{car['Specification']['Odometer']} km"
                year = f"{car['Specification']['YearFabrication']}/{car['Specification']['YearModel']}"

                title_formatted = f'{title}'
                value_formatted = f'R$ {price:,.2f}'.replace(",", ".").replace(".", ",", 1)

                if href not in links_existentes:
                    with open("links/linksWebmotors.txt", "a", encoding="utf-8") as file:
                        file.write(href + "\n")
                    data_car = [title_formatted, value_formatted, href, km, year]
                    data_for_telegram.append(data_car)

            if len(links_existentes) > 10000:
                links_existentes = links_existentes[-10000:]
                with open('links/linksWebmotors.txt', "w", encoding="utf-8") as file:
                    file.write("\n".join(links_existentes) + "\n")            
                                        
            return data_for_telegram
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar carros: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            self.driver.quit()
            raise Exception('Erro ao encontrar carros')
        
    def buildUrl(self, car):
        make = car['Specification']['Make']['Value'].lower()
        model = car['Specification']['Model']['Value'].lower()

        version_raw = car['Specification'].get('Version', {}).get('Value', '')
        version = (version_raw.lower()
                .replace(' ', '-')
                .replace('.', '') 
                .replace('/', '-')
                .replace('á', 'a')
                .replace('é', 'e')
                .replace('í', 'i')
                .replace('ó', 'o')
                .replace('ú', 'u')
                .replace('ç', 'c')
                .replace('ã', 'a')
                .replace('õ', 'o'))

        doors = car['Specification'].get('Doors', '')
        doors_formatted = f"{doors}-portas" if doors else "4-portas"

        year_fabrication = int(car['Specification']['YearFabrication'])
        year_model = int(car['Specification']['YearModel'])

        unique_id = car['UniqueId']

        href = (f"https://www.webmotors.com.br/comprar/{make}/{model}/{version}/"
                f"{doors_formatted}/{year_fabrication}-{year_model}/{unique_id}?pos=a{unique_id}c:&np=1")
        return href
