from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import subprocess
from selenium import webdriver
import traceback
import platform
import logging
from time import sleep
import datetime
import re
import os

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

class Olx:
    def process_link(self, link):
        logging.info('Abrindo site da OLX ---')
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
            try:
                sleep(1)
                self.driver.quit()
            except: pass
            return data_for_telegram
            
            
            # self.options = uc.ChromeOptions()
            # self.options.add_argument("--disable-infobars")
            # self.options.add_argument("--disable-extensions")
            # self.options.add_argument("--no-sandbox")
            # #self.options.add_argument("--headless") 
            # service = ChromeService(ChromeDriverManager().install())
            # self.driver = uc.Chrome(service=service, options=self.options)  
            # self.driver.get(link)
            # sleep(10)
                       
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao abrir site')
        
    def get_cars(self):
        try:
            with open('links/linksOlx.txt', "r", encoding="utf-8") as file:
                links_existentes = [line.strip().rstrip(",") for line in file]
            data_for_telegram = []
            
            for page in range(3):  
                logging.info('Procurando carros ---')
                sleep(10)
                selectors= [
                    'section[data-ds-component="DS-AdCard"]',
                    'section[data-mode="vertical"]'
                ]

                for selector in selectors:
                    cars = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(cars): break
                for car in cars:
                    try:
                        link_element = car.find_element(By.CSS_SELECTOR, "a")
                        title_element = car.find_element(By.CSS_SELECTOR, 'h2')
                        value_element = car.find_element(By.CSS_SELECTOR, 'h3')
                        km = car.find_elements(By.CSS_SELECTOR, '.olx-ad-card__labels-item')
                        km = km[0].text.strip()
                        value = value_element.text.strip()
                        title = title_element.text.strip()
                        href = link_element.get_attribute("href")
                        href_limpo = re.sub(r'[\?&]utm_[^=]+=[^&]+', '', href)
                        with open("links/linksOlx.txt", "a", encoding="utf-8") as file:
                            if href_limpo not in links_existentes:
                                file.write(href_limpo + ",\n")
                                data_car = [title, value, href_limpo, km]
                                data_for_telegram.append(data_car)
                                
                    except: continue
                    
                if len(links_existentes) > 2000:
                    links_existentes = links_existentes[-2000:]
                    with open('links/linksOlx.txt', "w", encoding="utf-8") as file:
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
                raise Exception('Erro ao encontrar carros')
            
    def second_page(self):
        try:
            logging.info('Indo para próxima página ---')
            botao = self.driver.find_element(By.CSS_SELECTOR, '.sc-5ebad952-1.wskjO')    
            self.driver.execute_script("arguments[0].scrollIntoView();", botao)
            sleep(5)
            botaos = self.driver.find_elements(By.CSS_SELECTOR, '.olx-core-button.olx-core-button--link.olx-core-button--small.sc-5ebad952-0.gVRVOX')
            for b in botaos:
                if b.text.strip() == '2':
                    b.click()
                    sleep(10)
                    self.page_second = True
                    break
    
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar botões: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao encontrar botões')
        
    def terceira_page(self):
        try:
            logging.info('Indo para próxima página ---')
            botao = self.driver.find_element(By.CSS_SELECTOR, '.sc-5ebad952-1.wskjO')    
            self.driver.execute_script("arguments[0].scrollIntoView();", botao)
            sleep(5)
            botaos = self.driver.find_elements(By.CSS_SELECTOR, '.olx-core-button.olx-core-button--link.olx-core-button--small.sc-5ebad952-0.gVRVOX')
            for b in botaos:
                if b.text.strip() == '3':
                    b.click()
                    sleep(10)
                    break
                
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar botões: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao encontrar botões')
                