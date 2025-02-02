from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import traceback
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
        try:
            logging.info('Abrindo site da OLX ---')
            self.options = uc.ChromeOptions()
            self.options.add_argument("--disable-infobars")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--no-sandbox")
            #self.options.add_argument("--headless") 
            service = ChromeService(ChromeDriverManager().install())
            self.driver = uc.Chrome(service=service, options=self.options)  
            self.driver.get(link)
            sleep(10)
            data_for_telegram = self.get_cars()
            try:
                sleep(1)
                self.driver.quit()
            except: pass
            return data_for_telegram
                       
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao abrir site')
        
    def get_cars(self):
        try:
            with open('links/linksOlx.txt', "r", encoding="utf-8") as file:
                links_existentes = [line.strip().rstrip(",") for line in file]
            data_for_telegram = []
            
            for page in range(2):  
                logging.info('Procurando carros ---')
                sleep(10)
                cars = self.driver.find_elements(By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]')
                for car in cars:
                    link_element = car.find_element(By.CSS_SELECTOR, "a[data-ds-component='DS-NewAdCard-Link']")
                    title_element = car.find_element(By.CSS_SELECTOR, 'h2')
                    value_element = car.find_element(By.CSS_SELECTOR, 'h3.olx-ad-card__price')
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
                
                if len(links_existentes) > 2000:
                    links_existentes = links_existentes[-2000:]
                    with open('links/linksOlx.txt', "w", encoding="utf-8") as file:
                        file.write("\n".join(links_existentes) + ",\n")
                            
                if page == 1: break
                self.second_page()
                sleep(5)
                
            return data_for_telegram
            
        except Exception as error:
                logging.error(f'Erro ao tentar encontrar carros: {error}')
                logging.error('Traceback: %s', traceback.format_exc())
                self.driver.quit()
                raise Exception('Erro ao encontrar carros')
            
    def second_page(self):
        try:
            logging.info('Indo para segunda página ---')
            botao = self.driver.find_element(By.CSS_SELECTOR, '.sc-5ebad952-1.wskjO')    
            self.driver.execute_script("arguments[0].scrollIntoView();", botao)
            sleep(5)
            botaos = self.driver.find_elements(By.CSS_SELECTOR, '.olx-core-button.olx-core-button--link.olx-core-button--small.sc-5ebad952-0.gVRVOX')
            for b in botaos:
                if b.text.strip() == '2':
                    b.click()
                    sleep(10)
                    break
        except Exception as error:
            logging.error(f'Erro ao tentar encontrar botões: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao encontrar botões')