from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import traceback
import logging
from time import sleep
import datetime
import os
import subprocess
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

class Webmotors:

    def process_link(self, link):
        
        # try:
        #     headers = {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        #         "Accept-Language": "pt-BR,pt;q=0.9",
        #         "Referer": "https://www.google.com/",
        #         "Connection": "keep-alive",
        #     }
        #     session = requests.Session()
        #     session.headers.update(headers)
        #     url = "https://www.webmotors.com.br/api/search/car?url=https%3A%2F%2Fwww.webmotors.com.br%2Fcarros%2Festoque%2Fonix%3Festadocidade%3Destoque%26marca1%3DCHEVROLET%26modelo1%3DONIX%26actualPage=1&displayPerPage=24&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false&pandora=false&mediaZeroKm=true"
        #     response = session.get(url)

        #     print(response)
        #     dados_json = response.json()
            
        #     self.get_cars(dados_json)                
        # except: pass
            
    # def construir_url(carro):
    #     marca = carro['marca'].lower()
    #     modelo = carro['modelo'].lower() 
    #     versao = carro['versao'].lower() 
    #     ano_modelo = carro['ano_modelo'].split('-')[0]  
    #     unique_id = carro['unique_id']

    #     if "turbo" in versao:
    #         motorizacao = "turbo-flex"
    #     elif "flex" in versao:
    #         motorizacao = "flex"
    #     elif "1.0" in versao:
    #         motorizacao = "1.0"
    #     else:
    #         motorizacao = "flex"  # Valor genérico caso a versão não tenha uma motorização clara
        
    #     # Montando o link no formato correto
    #     url = f"https://www.webmotors.com.br/comprar/{marca}/{modelo}/10-{motorizacao}-{versao}/4-portas/{ano_modelo}/{unique_id}?pos={unique_id}g:&np=1"
    #     return url
     
        try:
            system = platform.system()
      
            if system == "Windows":
                subprocess.Popen(
                    f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --log-level=3 --remote-debugging-port=9222', shell=True)
            elif system == "Linux":
                subprocess.Popen(
                    f'/usr/bin/google-chrome --log-level=3 --remote-debugging-port=9222', shell=True)
            
            sleep(1)
            service = Service()
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")         

            if system == "Windows":
                self.driver = webdriver.Chrome(service=service, options=self.options)
            elif system == "Linux":
                self.driver = webdriver.Chrome(service=service, options=self.options)
            
            self.driver.get(link)
            sleep(10)
            data_for_telegram = self.get_cars()
            try: self.driver.quit()
            except: pass
            return data_for_telegram
        
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception(f"Erro ao abrir site {error}")
        
    def get_cars(self, dados_json):
        try:
            logging.info('Procurando carros ---')
            sleep(10)
            
            # resultados = []
    
            # for item in dados_json.get('SearchResults', []):
            #     spec = item.get('Specification', {})
            #     prices = item.get('Prices', {})
            #     media  = item.get('Media', {})
                
            #     link_carro = item.get('URL', '')
                
            #     carro = {
            #         'title': spec.get('Title', 'Sem título'),
            #         'ano_modelo': spec.get('YearModel', ''),
            #         'versao': spec.get('Version', {}).get('Value', 'Sem versão'),
            #         'modelo': spec.get('Model', {}).get('Value', 'Sem modelo'),
            #         'transmissao': spec.get('Transmission', ''),
            #         'quilometragem': spec.get('Odometer', ''),
            #         'preco': prices.get('Price', ''),
            #         'link': link_carro
            #     }
                
            #     resultados.append(carro)
            # data_for_telegram =  self.filtrar(resultados)
                

            data_for_telegram = []
            cars = self.driver.find_elements(By.CSS_SELECTOR, '.sc-laTMn.hebMcT')
            for car in cars:
                link_element = car.find_element(By.CSS_SELECTOR, '.sc-kIPQKe.sc-eXEjpC.gXNwLQ')
                title_element = car.find_element(By.CSS_SELECTOR, '.sc-hqyNC.Vropq')
                subtitle_element = car.find_element(By.CSS_SELECTOR, '.sc-jbKcbu.fQZoiO')
                value_element = car.find_element(By.CSS_SELECTOR, '.sc-cJSrbW.ewMDbD')
                km_year = car.find_elements(By.CSS_SELECTOR, '.sc-cHGsZl.goowTJ')
                year = km_year[0].text.strip()
                km = km_year[1].text.strip()

                href = link_element.get_attribute("href")
                title = title_element.text.strip()
                subtitle = subtitle_element.text.strip()
                value = value_element.text.strip()
                title = f'{title} / {subtitle}'     
                with open("links/linksWebmotors.txt", "a", encoding="utf-8") as file:
                    if href not in links_existentes:
                        file.write(href + ",\n")
                        data_car = [title, value, href, km, year]
                        data_for_telegram.append(data_car)
                        
        except Exception as error:
                logging.error(f'Erro ao tentar encontrar carros: {error}')
                logging.error('Traceback: %s', traceback.format_exc())
                self.driver.quit()
                raise Exception('Erro ao encontrar carros')
            
    # def filtrar(self, results):
    #     logging.info('Filtrando carros ---')
    #     try:
    #         with open('links/linksWebmotors.txt', "r", encoding="utf-8") as file:
    #             links_existentes = [line.strip().rstrip(",") for line in file]
    #         data_for_telegram = []

    #         for carro in results:
    #             if carro['link'] not in links_existentes:
                               
    #                 title = carro['title']
    #                 value = carro['preco']
    #                 link = carro['link']
    #                 km = carro['quilometragem']
    #                 year = carro['ano_modelo']
    #                 file.write(link + ",\n")
    #                 data_car = [title, value, link, km, year]
    #                 data_for_telegram.append(data_car)
                    
        
        
    #         if len(links_existentes) > 2000:
    #                 links_existentes = links_existentes[-2000:]
    #                 with open('links/linksWebmotors.txt', "w", encoding="utf-8") as file:
    #                     file.write("\n".join(links_existentes) + ",\n")
                        
    #         return data_for_telegram
        
    #     except Exception as error:
    #         logging.error(f'Erro ao tentar filtrar carros: {error}')
    #         logging.error('Traceback: %s', traceback.format_exc())
    #         self.driver.quit()
    #         raise Exception('Erro ao filtrar carros')




    # def scrolar(self):
    #     logging.info('Rolando para baixo ---')        
    #     for _ in range(3):
    #         try:                
    #             self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    #             sleep(10)
    #         except Exception as error:
    #             logging.error(f'Erro ao tentar rolar: {error}')
    #             logging.error('Traceback: %s', traceback.format_exc())