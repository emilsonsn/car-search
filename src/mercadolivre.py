from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
import traceback
import logging
import subprocess
from time import sleep
import datetime
import platform
import os
import re

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

class MercadoLivre():
    def process_link(self, link):
        try:
            
            system = platform.system()
            
            self.options = [
                '--no-sandbox',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-infobars',
                '--log-level=3',
                '--remote-debugging-port=9222',
            ]            
            self.options = " ".join(self.options)            
            if system == "Windows":
                subprocess.Popen(
                    f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" {self.options}', shell=True)
            elif system == "Linux":
                subprocess.Popen(
                    f'/usr/bin/google-chrome {self.options}', shell=True)
            

                
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
            return data_for_telegram
            
            
            
            # logging.info('Abrindo site do Mercado Livre ---')
            # self.options = uc.ChromeOptions()
            # self.options.add_argument("--disable-infobars")
            # self.options.add_argument("--disable-extensions")
            # self.options.add_argument("--no-sandbox")
            # self.options.add_argument("--headless") 
            # service = ChromeService(ChromeDriverManager().install())
            # self.driver = uc.Chrome(service=service, options=self.options)  
            # self.driver.get(link)
            # sleep(10)
            # data_for_telegram = self.get_cars()
            # try: self.driver.quit()
            # except: pass
            # return data_for_telegram
         
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao abrir site')
    
    def get_cars(self):
        try:
            with open('links/linksML.txt', "r", encoding="utf-8") as file:
                links_existentes = [line.strip().rstrip(",") for line in file]
            data_for_telegram = []     
        
            for page in range(3):
                logging.info('Procurando carros ---')
                sleep(10)
                li_list = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')
                for li in li_list:
                    link_element = li.find_element(By.CSS_SELECTOR, '.poly-component__title')
                    value_element = li.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction')
                    km_year = li.find_elements(By.CSS_SELECTOR, '.poly-attributes-list__item.poly-attributes-list__separator')
                    year = km_year[0].text
                    km = km_year[1].text
                    href = link_element.get_attribute("href")
                    title = link_element.get_attribute("text")
                    value = value_element.text.strip() 
                    href_limpo = re.sub(r'#.*', '', href)
                    
                    with open("links/linksML.txt", "a", encoding="utf-8") as file:
                        if href_limpo not in links_existentes:
                            file.write(href_limpo + ",\n")
                            data_car = [title, value, href_limpo, km, year]
                            data_for_telegram.append(data_car)
                            
                if len(links_existentes) > 2000:
                    links_existentes = links_existentes[-2000:]
                    with open('links/linksML.txt', "w", encoding="utf-8") as file:
                        file.write("\n".join(links_existentes) + ",\n")
                            
                if page == 2: break
                elif page == 1: self.terceira_page()
                else: self.second_page()
                                                
                sleep(5)
            return data_for_telegram
        
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar carros: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            self.driver.quit()
            raise Exception('Erro ao encontrar links')
        
    def second_page(self):
        logging.info('Abrindo segunda página ---')
        sleep(2)
        botao = self.driver.find_element(By.CSS_SELECTOR, '.andes-pagination.ui-search-andes-pagination.andes-pagination--large')                        
        self.driver.execute_script("arguments[0].scrollIntoView();", botao)
        sleep(5)
        botaos = self.driver.find_elements(By.CSS_SELECTOR, '.andes-pagination__link')
        for b in botaos:
            if b.text.strip() == '2':
                b.click()
                sleep(10)
                break
                
    def terceira_page(self):
        try:
            logging.info('Indo para próxima página ---')
            botao = self.driver.find_element(By.CSS_SELECTOR, '.andes-pagination.ui-search-andes-pagination.andes-pagination--large')                        
            self.driver.execute_script("arguments[0].scrollIntoView();", botao)
            sleep(5)
            botaos = self.driver.find_elements(By.CSS_SELECTOR, '.andes-pagination__link')
            for b in botaos:
                if b.text.strip() == '3':
                    b.click()
                    sleep(10)
                    break
                
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar botões: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao encontrar botões')