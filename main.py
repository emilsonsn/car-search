from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from src.mercadolivre import MercadoLivre
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
            self.mercadolivre = MercadoLivre()
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
        # site = 'OLX'
        
        
        # link_olx = 'https://www.olx.com.br/brasil?q=onix'
        link_ml = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/chevrolet/onix/#D[A:onix]'
        
        links_for_telegram_ML = self.mercadolivre.process_link(link_ml)        
        # data_for_telegram_OLX = self.olx.process_link(link_olx)


            
            
        pass
            
            
        
        
    
    def send_results_telegram(self, results, groups):
        for link in results:
            
            message = f"Montar mensagem usando {link}"

            self.telegram.send_message(groups, message)

    
    def main(self):
        # self.olx.process_link(link)
        
        
        
        
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


