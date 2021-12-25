import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from random import randint
from intents import detect_intent_texts


def support(event, vk_api):
    response_intent = detect_intent_texts(
        project_id='kruser-support-bot',
        session_id=event.user_id,
        texts=event.text,
        language_code='ru-RU'
    )

    if response_intent.action == 'input.unknown':
        return
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_intent.fulfillment_text,
            random_id=randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.environ['TOKEN_GROUP_VK']

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            support(event, vk_api)
