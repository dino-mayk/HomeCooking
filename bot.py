from telegram.ext import CommandHandler
import logging
from telegram.ext import Updater, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TOKEN = '5386269245:AAGDVEgztCLzjZpjpwVAFm-D1G-1z54_2cc'


def start(update, context):
    update.message.reply_text(
        "Вступление")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать...")


def send(update, context):
    update.message.reply_text('привет')


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("send", send))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()