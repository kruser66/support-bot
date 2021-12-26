import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from intents import detect_intent_texts
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('support-bot')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот поддержки ответит на Ваши вопросы')


def support(update: Update, context: CallbackContext) -> None:
    response_intent = detect_intent_texts(
        project_id=context.bot_data['google_project_id'],
        session_id=update.message.chat['id'],
        texts=update.message.text,
        language_code='ru-RU'
    )
    if response_intent.intent.is_fallback:
        # TODO обработчик "неизвестных" запросов
        logger.info(f'TG_BOT: неизвестный запрос - "{update.message.text}"')
    else:
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
    google_project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    try:
        updater = Updater(token=tg_token)
        dispatcher = updater.dispatcher
        dispatcher.bot_data = {
            'google_project_id': google_project_id,
        }

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, support)
        )

        updater.start_polling()

        updater.idle()
    except Exception:
        logger.exception('TG_BOT')


if __name__ == '__main__':
    main()
