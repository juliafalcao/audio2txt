#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config.bot import bot_token
from requests import get

from src.audio import download_and_transcribe

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chat_id(update):
    return update.message.chat.id

def start(update, context):
    logging.info("Received /start")
    update.message.reply_text('Hi!')

def echo(update, context):
    logging.info("Received text message")
    update.message.reply_text(update.message.text)

def transcribe(update, context):
    logging.info("Received voice message!")
    chat_id = update.message.chat.id 
    file_id = update.message.voice.file_id
    file_size = update.message.voice.file_size # TODO: verify

    txt = download_and_transcribe(file_id, chat_id)
    logging.info("Text: %s" % txt)


def main():
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(MessageHandler(Filters.voice, transcribe))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
