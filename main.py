from src.mercadolivre import MercadoLivre
from src.webmotors import Webmotors
from src.telegram import TelegramBot
from src.icarros import ICarros
from src.olx import Olx
from time import sleep
import traceback
import requests
import datetime
import logging
import json
import os
import platform

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

class Main:
    def __init__(self):
        try:
            logging.info('Inicializando bot---')
            self.telegram = TelegramBot()
            self.telegram.start()

            self.olx = Olx()
            self.webmotors = Webmotors()
            self.mercadolivre = MercadoLivre()
            self.icarros = ICarros()
            self.api_url = 'https://roccoveiculos.online/api'

        except Exception as error:
            logging.error(f'Erro ao iniciar: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao carregar dados')
    
    def getLinks(self):     
        print('Buscando links...')
        response = requests.get(f"{self.api_url}/links")
        result = response.json() 

        if not result['status']: 
            exit(1)
            pass
        links = result['data']

        print(f"Links achados: {len(links)}")

        return links

    def send_results_telegram(self, results, site, groups):
        def format_message(batch):
            
            message = f"🚗 *Novos anúncios em {site.upper()}* 🚗\n\n"
            for i, result in enumerate(batch, start=1):
                title = result[0]
                value = result[1]
                link = result[2]
                km = result[3]
                try: year = result[4]
                except IndexError:
                    year = '------'
                message += (f"🔹 *{title}*\n"
                            f"💰 *Preço:* {value}\n"
                            f"🚗 *Km:* {km}\n"
                            f"📅 *Ano:* {year}\n"
                            f"🔗 [Ver anúncio]({link})\n"
                            "-----------------------------\n")
            return message
        
        batch_size = 10
        for i in range(0, len(results), batch_size):
            batch = results[i:i + batch_size]
            formatted_message = format_message(batch)            
            self.telegram.send_message(formatted_message,groups)
            sleep(1)

    def close_chrome(self):
        system = platform.system()
        try:
            if system == "Windows":
                os.system("taskkill /F /IM chrome.exe")
            elif system == "Linux":
                os.system("pkill chrome")
        except Exception as e:
            print(f"Erro ao tentar fechar o Chrome: {e}")

    def main(self):
        while True:
            # link = 'https://www.webmotors.com.br/carros/estoque/ram?estadocidade=estoque&marca1=RAM&autocomplete=RAM&autocompleteTerm=RAM&lkid=1704'
            # self.webmotors.process_link(link)
            
            links = self.getLinks()
            for link in links:
                self.close_chrome()
                sleep(5)
                try:
                    url = link['url']
                    site = link['site']
                    if site == 'olx':
                        print('Iniciando olx')
                        results = self.olx.process_link(url)
                    elif site == 'webmotos':
                        print('Iniciando webmotors')
                        results = self.webmotors.process_link(url)
                    elif site == 'mercadolivre':
                        print('Iniciando mercadolivre')
                        results = self.mercadolivre.process_link(url)
                    elif site == 'icarros':
                        print('Iniciando icarros')
                        results = self.icarros.process_link(url)                
                    else: return         
    
                    groups = json.loads(link['groups'])
    
                    if(len(results)):
                        print('Iniciando disparo de mensagens no telegram')
                        self.send_results_telegram(results, site, groups)
                    sleep( 60 * 1 )
                except Exception as e:
                    logging.info(f'erro {e}')                    
            logging.info('Esperando 5 minutos ---')
        
            sleep( 60 * 5 )
            
if __name__ == "__main__":
    main = Main()
    main.main()
