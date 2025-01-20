import requests
import json
from src.olx import Olx
from src.webmotors import Webmotors
from src.telegram import Telegram
from time import sleep

class Main:

    def __init__(self):
        config  = json.load(open('config.json'))
        self.telegram = Telegram()
        self.telegram.start(config['telegram_token'])

        self.olx = Olx()
        self.webmotors = Webmotors()
        # ... continuar para o restante dos sites
    
    def getLinks(self):
        request = requests.get('http://dominio.com.br/get-links')
        result = json.loads(request)

        if not result['status']: 
            # log de erro | parar o projeto
            exit(1)
            pass

        links = result['data']
    
    def send_results_telegram(self, results, groups):
        for link in results:
            
            message = f"Montar mensagem usando {link}"

            self.telegram.send_message(groups, message)

    
    def main(self):
        links = self.getLinks()

        for link in links:
            if link['site'] == 'olx':
                results = self.olx.process_link(link)
            elif link['site'] == 'webmotos':
                results = self.webmotors.process_link(link)
            # ... continuar para o restante dos sites

            self.send_results_telegram(results, link['groups'])
        
        sleep(60)
            
if __name__ == "__main__":
    main = Main()
    main.main()


