from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import traceback
import logging
from time import sleep
import datetime
import os

data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
os.makedirs('logs', exist_ok=True)
logging.basicConfig(level=logging.INFO, filename=f'logs/app_{data_atual}.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

class Webmotors:

    def process_link(self, link):
        try:
            logging.info('Abrindo site Webmotors ---')
            self.options = uc.ChromeOptions()
            self.options.add_argument("--disable-infobars")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--window-size=1920,1080")
            self.options.add_argument("--disable-blink-features=AutomationControlled")

            service = ChromeService(ChromeDriverManager().install())
            self.driver = uc.Chrome(service=service, options=self.options)  
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
            cars = self.driver.find_elements(By.CSS_SELECTOR, '.sc-laTMn.hebMcT')
            for car in cars:
                link_element = car.find_element(By.CSS_SELECTOR, '.sc-kIPQKe.sc-eXEjpC.gXNwLQ')
                title_element = car.find_element(By.CSS_SELECTOR, '.sc-hqyNC.Vropq')
                subtitle_element = car.find_element(By.CSS_SELECTOR, '.sc-jbKcbu.fQZoiO')
                value_element = car.find_element(By.CSS_SELECTOR, '.sc-cJSrbW.ewMDbD')
                href = link_element.get_attribute("href")
                title = title_element.text.strip()
                subtitle = subtitle_element.text.strip()
                value = value_element.text.strip()
                title = f'{title} / {subtitle}'     
                with open("links/linksWebmotors.txt", "a", encoding="utf-8") as file:
                    if href not in links_existentes:
                        file.write(href + ",\n")
                        data_car = [title, value, href]
                        data_for_telegram.append(data_car)
                        
            if len(links_existentes) > 500:
                links_existentes = links_existentes[-250:] 
                with open('links/linksWebmotors.txt', "w", encoding="utf-8") as file:
                    for link in links_existentes:
                        file.write(link + ",\n")
                 
            return data_for_telegram
                           
        except Exception as error:
                logging.error(f'Erro ao tentar encontrar carros: {error}')
                logging.error('Traceback: %s', traceback.format_exc())
                self.driver.quit()
                raise Exception('Erro ao encontrar carros')