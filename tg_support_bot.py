import os
import logging
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from intents import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот поддержки ответит на Ваши вопросы')


def support(update: Update, context: CallbackContext) -> None:
    response_intent = detect_intent_texts(
        'kruser-support-bot',
        update.message.chat['id'],
        update.message.text,
        'ru-RU'
    )
    if response_intent.action != 'input.unknown':
        update.message.reply_text(response_intent.fulfillment_text)


class TgLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    tg_token = os.environ['TG_BOT_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_bot = Bot(token=tg_token)

    logger.addHandler(TgLogsHandler(tg_bot, tg_chat_id))

    os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, support)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
