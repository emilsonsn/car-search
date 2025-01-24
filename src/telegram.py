from time import sleep
import telebot

from datetime import datetime

class TelegramBot:
    
    def start(self, token):
        self.token = token        
        self.bot = telebot.TeleBot(self.token, parse_mode=None)        

    def send_message(self, mensagem, grupos):
        for g, grupo in enumerate(grupos):
            try:
                self.bot.send_message(f"-100{grupo}", mensagem, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as err:
                print(err)
                continue        
        