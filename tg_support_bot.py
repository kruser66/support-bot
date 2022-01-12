import os
from tg_logs_handler import *
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from dialogflow_intents import detect_intent_texts
import logging
from requests import (
    ReadTimeout,
    ConnectTimeout,
    HTTPError,
    Timeout,
    ConnectionError
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

    update.message.reply_text(response_intent.fulfillment_text)


def main():
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TgLogsHandler(tg_bot, tg_chat_id))

    google_project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data = {
        'google_project_id': google_project_id,
    }

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, support)
    )
    try:
        updater.start_polling()
        updater.idle()
    except (
        ReadTimeout,
        ConnectTimeout,
        HTTPError,
        Timeout,
        ConnectionError
    ) as error:
        logger.exception(f'TG_BOT: {error}')


if __name__ == '__main__':
    main()
