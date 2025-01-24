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
from src.telegram import TelegramBot
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
            self.config = self.getConfigs()
            self.telegram = TelegramBot()
            self.telegram.start(self.config['telegram_token'])

            self.olx = Olx()
            self.webmotors = Webmotors()
            self.mercadolivre = MercadoLivre()
            # ... continuar para o restante dos sites

        except Exception as error:
            logging.error(f'Erro ao iniciar: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao carregar dados')
    
    def getConfigs(self):
        # request.get('https://dominio.com.br/configs')
        # result = json.loads(request)

        # if not result['status']: 
        #     # log de erro | parar o projeto
        #     exit(1)
        # return result['data']
        return {
            'telegram_token': '7870776836:AAHxEaY3qH_Wa3OevIUkJIn0Ha2JZb-kFlY'
        }
        pass
    
    def getLinks(self):        
        # result = json.loads(request)

        # if not result['status']: 
        #     # log de erro | parar o projeto
        #     exit(1)
        #     pass
        # links = result['data']
        # site = 'OLX'
        
        links = [
            {
                "site": 'mercadolivre',
                "url": 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/chevrolet/onix/#D[A:onix]',
                "groups": ['2452087430']
            },
            {
                "site": "olx",
                "url": 'https://www.olx.com.br/brasil?q=onix',
                "groups": ['1111']
            }                        
        ]

        return links

    def send_results_telegram(self, results, site, groups):
        def format_message(batch):
            message = f"🚗 *Novos anúncios em {site.upper()}* 🚗\n\n"
            for i, result in enumerate(batch, start=1):
                title = result[0]
                value = result[1]
                link = result[2]
                message += (f"🔹 *{title}*\n"
                            f"💰 *Preço:* {value}\n"
                            f"🔗 [Ver anúncio]({link})\n"
                            "-----------------------------\n")
            return message
        
        batch_size = 10
        for i in range(0, len(results), batch_size):
            batch = results[i:i + batch_size]
            formatted_message = format_message(batch)            
            self.telegram.send_message(formatted_message,groups)
            sleep(1)

    def main(self):
        # self.olx.process_link(link)
        self.webmotors.process_link('https://www.webmotors.com.br/carros/estoque/chevrolet/onix?estadocidade=estoque&marca1=CHEVROLET&modelo1=ONIX&autocomplete=onix')

        links = self.getLinks()

        for link in links:
            url = link['url']
            site = link['site']
            if site == 'olx':
                results = self.olx.process_link(url)
            elif site == 'webmotos':
                results = self.webmotors.process_link(url)
            elif site == 'mercadolivre':
                results = self.mercadolivre.process_link(url)
            else: return         

            if(len(results)): self.send_results_telegram(results, site, link['groups'])
        
        sleep(60)
            
if __name__ == "__main__":
    main = Main()
    main.main()