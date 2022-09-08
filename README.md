# Бот-помощник

Представленный бот реализует функцию бота-помощника, который отвечает на популярные вопросы, а что-то посложнее переводит на операторов. Бот доступен для сервисов ВКонтакте и Телеграм.

Для ответов на типичные вопросы бот пользуется [DialogFlow](https://cloud.google.com/dialogflow/docs) - платформой на Google Cloud Services.

## Installation and Environment setup

У вас должен быть установлен python3.

Вы можете использовать команду `pip` (или `pip3`, чтобы избежать конфликта с Python2) для установки зависимостей.
```
pip install -r requirements.txt
```

Этот скрипт использует файл `.env` в корневой папке, чтобы хранить переменные, которые нужны для успешной работы скрипта. Вам нужно его создать самостоятельно.

Внутри вашего файла `.env` вы можете указать следующие переменные:

`TG_TOKEN`=Токен телеграм-бота
`GOOGLE_APPLICATION_CREDENTIALS`=Путь к JSON-файлу, в котором лежат данные для аутентификации в Google Clod Services
`PROJECT_ID`=Уникальный идентификатор вашего проекта в DialogFlow, созданного с помощью Google Cloud Services
`VK_TOKEN`=Токен группы ВКонтакте, с которой будет общаться пользователь
`LOGGER_TG_TOKEN`=Токен телеграм-бота, в котором будут отображаться ошибки в случае их появлениях в ботах
`LOGGER_CHAT_ID`=Ваш ID в телеграме, чтобы скрипт понимал кому слать сообщения о неправильной работе ботов

Для успешной работы скрипта вам надо создать IalogFlow и связать его с проектом Google. Вы можете обратиться к [официальному руководству](https://cloud.google.com/dialogflow/es/docs/quick/setup) для начальной настройки и создания агента. Возможно, вам также понадобится создать [сервисный аккаунт](https://cloud.google.com/dialogflow/es/docs/quick/setup#sa-create) и [получить скрытые ключи](https://cloud.google.com/dialogflow/es/docs/quick/setup#auth-env).

Вам нужно будет настроить агент DialogFlow, чтобы управлять потоком разговора. Следуйте инструкциям [официальной документации](https://cloud.google.com/dialogflow/es/docs/quick/build-agent), чтобы сделать это.

Чтобы не создавать диалоговые потоки самостоятельно вы можете воспользоваться скриптом `create_intent.py`.

Если вы не знаете как получить токен телегра-бота, вы может воспользоваться [официальным руководством](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

Если вы не знаете как получить токен доступа к группе ВКонтакте, вы можете найти его [здесь](https://dev.vk.com/api/community-messages/getting-started#Получение%20ключа%20доступа%20в%20настройках%20сообщества).

## Запуск

Используйте `tg_bot.py` для запуска телеграм-бота:

```
python tg_bot.py 
```

Используйте `vk_bot.py` для запуска бота для ВКонтакте:

```
python vk_bot.py 
```

Для массового создания диалоговых потоков в DialogFlow вы можете воспользоваться скриптом `create_intent.py`. Вам нужно создать JSON-файл под названием `training_phrases.json` в корневой папке проекта со следующей схемой:

```JavaScript
{
    "название диалогового потока": {
        "questions": [
            "Пример вопроса №1",
            "Пример вопроса №2",
            ... ,
            "Пример вопроса N"
        ],
        "answer": "Полный ответ"
    },
    ...
}
```

После того как создадите файл с нужным вам содержимым, воспользуйтесь следующей командой и в DialogFlow оздадутся новые потоки:

```
python create_intent.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).