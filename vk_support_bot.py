import os
import logging
import vk_api as vk
from telegram import Bot
from tg_logs_handler import TgLogsHandler
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from random import randint
from dialogflow_intents import detect_intent_texts
from requests import (
    ReadTimeout,
    ConnectTimeout,
    HTTPError,
    Timeout,
    ConnectionError
)


logger = logging.getLogger('vk-support-bot')


def support(event, vk_api, project_id):
    response_intent = detect_intent_texts(
        project_id=project_id,
        session_id=event.user_id,
        texts=event.text,
        language_code='ru-RU'
    )

    if response_intent.intent.is_fallback:
        # TODO обработчик "неизвестных" запросов
        logger.info(f'VK_BOT: неизвестный запрос - "{event.text}"')
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_intent.fulfillment_text,
            random_id=randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    # Telegram chat_id Администратора для мониторинга
    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_BOT_TOKEN']

    tg_bot = Bot(token=tg_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TgLogsHandler(tg_bot, tg_chat_id))

    vk_token = os.environ['VK_GROUP_TOKEN']
    google_project_id = os.environ['GOOGLE_CLOUD_PROJECT_ID']

    try:
        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                support(event, vk_api, google_project_id)
    except (
        ReadTimeout,
        ConnectTimeout,
        HTTPError,
        Timeout,
        ConnectionError
    ) as error:
        logger.exception(f'VK_BOT: Ошибка requests {error}')
