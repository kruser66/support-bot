import os
import logging
from telegram import Bot
from dotenv import load_dotenv

class TgLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


load_dotenv()
# Telegram chat_id Администратора для мониторинга
tg_chat_id = os.environ['TG_CHAT_ID']
tg_token = os.environ['TG_BOT_TOKEN']

tg_bot = Bot(token=tg_token)
