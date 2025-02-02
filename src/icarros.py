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

class ICarros:
    
    def process_link(self, link):
        try:
            logging.info('Abrindo site da ICarros ---')
            self.options = uc.ChromeOptions()
            self.options.add_argument("--disable-infobars")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--headless")
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
                div_info = car.find_element(By.CSS_SELECTOR, '.offer-card__info')
                km_year = div_info.find_element(By.CSS_SELECTOR, '.info-container__car-info')
                km_year = km_year.text.split('\n')
                
                year = km_year[0].strip()
                km = km_year[1].strip()
                href = link_element.get_attribute('href')
                href = re.sub(r'\?(pos=\d+&?|hfv=\w+&?|financiamento=\w+&?)*$', '', href)
                title = title_element.text.strip()
                subtitle = subtitle_element.text.strip()
                value = value_element.text
                title = f'{title} / {subtitle}'
                with open("links/linksIcarros.txt", "a", encoding="utf-8") as file:
                    if href not in links_existentes:
                        file.write(href + ",\n")
                        data_car = [title, value, href, km, year]
                        data_for_telegram.append(data_car)
                
            if len(links_existentes) > 2000:
                links_existentes = links_existentes[-2000:]
                with open('links/linksIcarros.txt', "w", encoding="utf-8") as file:
                    file.write("\n".join(links_existentes) + ",\n")
                            
            return data_for_telegram
                        
        except Exception as error:
            logging.error(f'Erro ao buscar carros: {error}')
            logging.error('Traceback: %s', traceback.format_exc())
            self.driver.quit()
            raise Exception('Erro ao buscar carros')