import telebot

class Telegram:
    def start(self, token):
        self.token = token
        self.bot = telebot.TeleBot(self.token)
    
    def send_message(self, groups, message):
        for group in groups:
            self.bot.send_message(group, message)
