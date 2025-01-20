from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from src.webmotors import Webmotors
from src.telegram import Telegram
from selenium import webdriver
from src.olx import Olx
from time import sleep
import traceback
import requests
import datetime
import logging
import json
import os

data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
os.makedirs('logs', exist_ok=True)
logging.basicConfig(level=logging.INFO, filename=f'logs/app_{data_atual}.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


class Main:


    def __init__(self):
        try:
            logging.info('Inicializando bot---')
            config  = json.load(open('config.json'))
            # self.telegram = Telegram()
            # self.telegram.start(config['telegram_token'])

            self.olx = Olx()
            self.webmotors = Webmotors()
            # ... continuar para o restante dos sites

        except Exception as error:
            logging.error(f'Erro ao iniciar: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao carregar dados')
    
    def getLinks(self):        
        # result = json.loads(request)

        # if not result['status']: 
        #     # log de erro | parar o projeto
        #     exit(1)
        #     pass
        # links = result['data']
        site = 'OLX'
        link = 'https://www.olx.com.br/brasil?q=onix'
        
        self.options = uc.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = uc.Chrome(service=service, options=self.options)  
        self.driver.get(link)
        sleep(2)
        cars = self.driver.find_elements(By.CSS_SELECTOR, '.olx-ad-card.olx-ad-card--horizontal.olx-ad-card--highlight')
        for i in cars:
            print(i.text)
            print(12)
        
        
        
        
        
        pass
    
    def send_results_telegram(self, results, groups):
        for link in results:
            
            message = f"Montar mensagem usando {link}"

            self.telegram.send_message(groups, message)

    
    def main(self):
        links = self.getLinks()

        for link in links:
            if link['site'] == 'olx':
                results = self.olx.process_link(link)
            elif link['site'] == 'webmotos':
                results = self.webmotors.process_link(link)
            # ... continuar para o restante dos sites

            self.send_results_telegram(results, link['groups'])
        
        sleep(60)
            
if __name__ == "__main__":
    main = Main()
    main.main()


