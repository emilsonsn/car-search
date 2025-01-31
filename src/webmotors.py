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
        
    def get_cars(self):
        try:
            with open('links/linksWebmotors.txt', "r", encoding="utf-8") as file:
                links_existentes = [line.strip().rstrip(",") for line in file]
            data_for_telegram = []
            
            logging.info('Procurando carros ---')
            sleep(10)
            self.scrolar()
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
                        
            if len(links_existentes) > 2000:
                links_existentes = links_existentes[-2000:]
                with open('links/linksWebmotors.txt', "w", encoding="utf-8") as file:
                    file.write("\n".join(links_existentes) + ",\n")
                 
            return data_for_telegram
                           
        except Exception as error:
                logging.error(f'Erro ao tentar encontrar carros: {error}')
                logging.error('Traceback: %s', traceback.format_exc())
                self.driver.quit()
                raise Exception('Erro ao encontrar carros')
            
    def scrolar(self):
        logging.info('Rolando para baixo ---')        
        for _ in range(3):
            try:                
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(10)
            except Exception as error:
                logging.error(f'Erro ao tentar rolar: {error}')
                logging.error('Traceback: %s', traceback.format_exc())