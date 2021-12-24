import os
import logging
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from pprint import pprint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def detect_intent_texts(project_id, session_id, texts, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(
        text=texts,
        language_code=language_code
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот поддержки ответит на Ваши вопросы')


def support(update: Update, context: CallbackContext) -> None:
    response_intent = detect_intent_texts(
        'kruser-support-bot',
        update.message.chat['id'],
        update.message.text,
        'ru-RU'
    )
    pprint(response_intent)
    if response_intent.action == 'input.unknown':
        logger.info(f'Неизвестный запрос: {update.message.text}')
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
