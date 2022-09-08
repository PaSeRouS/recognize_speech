import logging

from environs import Env
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext import CallbackContext

from dialog_flow_functions import detect_intent_texts
from log_handler import TelegramLogHandler

log = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_html(
        f"Привет, {user.mention_html()}!"
    )


def send_message(update: Update, context: CallbackContext):
    env = Env()
    env.read_env()

    project_id = env('PROJECT_ID')
    text = update.message.text
    chat_id = update.effective_chat.id

    response = detect_intent_texts(
            project_id,
            chat_id,
            text,
            'ru-RU'
        )

    update.message.reply_text(
        response.fulfillment_text
    )


def error(updat: object, context: CallbackContext):
    log.exception('Во время отправки сообщения произошла ошибка.')


def main():
    """Start the bot."""
    env = Env()
    env.read_env()

    tg_token = env('TG_TOKEN')

    logging.basicConfig(level=logging.WARNING)
    log.setLevel(logging.ERROR)
    log.addHandler(
        TelegramLogHandler(env('LOGGER_TG_TOKEN'), env('LOGGER_CHAT_ID'))
    )

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
