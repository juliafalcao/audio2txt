# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import boto3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bad = "bad"
ok = "ok"
good = "good"

replies = {
    bad: "Obrigada pelo feedback! Sinto muito que a transcrição não foi satisfatória 😣",
    ok: "Muito obrigada pelo feedback! 😊",
    good: "Muito obrigada pelo feedback! 😊"
}

def get_reply_markup():
    keyboard = [[
        InlineKeyboardButton("ruim", callback_data=bad),
        InlineKeyboardButton("ok", callback_data=ok),
        InlineKeyboardButton("boa!", callback_data=good)
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def handle_rating_callback(update, context):
    try:
        query = update.callback_query
        query.answer()
        chat_id = update.callback_query.message.chat.id
        query.edit_message_reply_markup(reply_markup=None) # hide inline keyboard
        context.bot.send_message(chat_id, text=replies[query.data]) # reply to feedback

    except Exception as e:
        logging.exception("handle_rating_callback - Exception: %s", str(e), exc_info=True)
