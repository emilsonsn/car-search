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
logging.basicConfig(level=logging.INFO, filename=f'logs/app_{data_atual}.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

class ICarros:
    
    def process_link(self, link):
        try:
            logging.info('Abrindo site da ICarros ---')
            self.options = uc.ChromeOptions()
            self.options.add_argument("--start-maximized")
            self.options.add_argument("--disable-infobars")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--headless")
            service = ChromeService(ChromeDriverManager().install())
            self.driver = uc.Chrome(service=service, options=self.options)  
            self.driver.get(link)
            sleep(2)
            data_for_telegram = self.get_cars()
            self.driver.quit()
            return data_for_telegram
        
        except Exception as error:
            logging.error(f'Erro ao abrir site: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao abrir site')
        

    def get_cars(self):
        try:
            with open('links/linksIcarros.txt', "r", encoding="utf-8") as file:
                links_existentes = [line.strip().rstrip(",") for line in file]
            data_for_telegram = []
            
            logging.info('Procurando carros ---')
            sleep(10)
            
            cars = self.driver.find_elements(By.CSS_SELECTOR, '.offer-card')
            for car in cars:
                div_title = car.find_element(By.CSS_SELECTOR, '.offer-card__header')
                link_element = car.find_element(By.CSS_SELECTOR, '.offer-card__title-container')
                title_element = div_title.find_element(By.CSS_SELECTOR, '.label__onLight.ids_textStyle_label_medium_bold')
                subtitle_element = div_title.find_element(By.CSS_SELECTOR, '.label__neutral.ids_textStyle_label_xsmall_regular')
                div_value = car.find_element(By.CSS_SELECTOR, '.offer-card__price-container')
                value_element = div_value.find_element(By.CSS_SELECTOR, '.label__onLight.ids_textStyle_label_medium_bold')
                href = link_element.get_attribute('href')
                href = re.sub(r'\?(pos=\d+&?|hfv=\w+&?|financiamento=\w+&?)*$', '', href)
                title = title_element.text.strip()
                subtitle = subtitle_element.text.strip()
                value = value_element.text
                title = f'{title} / {subtitle}'
                with open("links/linksIcarros.txt", "a", encoding="utf-8") as file:
                    if href not in links_existentes:
                        file.write(href + ",\n")
                        data_car = [title, value, href]
                        data_for_telegram.append(data_car)
                
            if len(links_existentes) > 500:
                links_existentes = links_existentes[-250:] 
                with open('links/linksIcarros.txt', "w", encoding="utf-8") as file:
                    for link in links_existentes:
                        file.write(link + ",\n")
                            
                            
            return data_for_telegram
                        
                            
                            
                
        except Exception as error:
            logging.error(f'Erro ao buscar carros: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            raise Exception('Erro ao buscar carros')
        
    
    