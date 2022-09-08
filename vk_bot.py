import logging
import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_functions import detect_intent_texts
from log_handler import TelegramLogHandler

log = logging.getLogger(__file__)


def handle_message(event, vk_api, project_id):
    chat_id = random.randint(1,1000)

    response = detect_intent_texts(
        project_id,
        chat_id,
        event.text,
        'ru-RU'
    )

    if not response.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.fulfillment_text,
            random_id=chat_id
        )


def main():
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    project_id = env('PROJECT_ID')

    logging.basicConfig(level=logging.WARNING)
    log.setLevel(logging.ERROR)
    log.addHandler(
        TelegramLogHandler(env('LOGGER_TG_TOKEN'), env('LOGGER_CHAT_ID'))
    )

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                handle_message(event, vk_api, project_id)
            except Exception:
                log.exception('Произошла ошибка во время отправки сообщения.')


if __name__ == "__main__":
    main()