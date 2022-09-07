from environs import Env
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext import CallbackContext

from dialog_flow_functions import detect_intent_texts


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_html(
        f"Привет, {user.mention_html()}!"
    )


def echo(update: Update, context: CallbackContext):
    env = Env()
    env.read_env()

    project_id = env('PROJECT_ID')
    text = update.message.text
    chat_id = update.effective_chat.id
    update.message.reply_text(
        detect_intent_texts(
            project_id,
            chat_id,
            text,
            'ru-RU'
        )
    )


def main():
    """Start the bot."""
    env = Env()
    env.read_env()

    tg_token = env('TG_TOKEN')

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
