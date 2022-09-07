import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_functions import detect_intent_texts


def echo(event, vk_api, project_id):
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
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, project_id)


if __name__ == "__main__":
    main()