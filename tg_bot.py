from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext import CallbackContext


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


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


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
