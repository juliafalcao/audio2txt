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
        # InlineKeyboardButton("💩", callback_data=bad),
        # InlineKeyboardButton("🤔", callback_data=ok),
        # InlineKeyboardButton("👌", callback_data=good),
        InlineKeyboardButton("ruim", callback_data=bad),
        InlineKeyboardButton("ok", callback_data=ok),
        InlineKeyboardButton("boa!", callback_data=good)
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def handle_rating_callback(update, context):
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat.id
    context.bot.send_message(chat_id, text=replies[query.data]) # reply to feedback
    query.edit_message_reply_markup(reply_markup=None) # hide inline keyboard

    save_rating(query.data, chat_id)

def save_rating(rating, chat_id):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f"{ts},{chat_id},{rating}\n"

    with open("log/reviews.csv", mode="a+", encoding="utf-8") as f:
        f.write(row)

def upload_ratings():
    logging.info("[S3] Uploading reviews.csv...")
    ts = datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
    s3_client = boto3.client("s3", region_name="sa-east-1")
    ok = False
    try:
        s3_filename = f"reviews/reviews_{ts}.csv"
        s3_client.upload_file("log/reviews.csv", "audio2txt", s3_filename)
        logging.info("[S3] Reviews uploaded (%s)", s3_filename)
        ok = True
    except Exception as e:
        logging.exception("[S3] Exception: %s", str(e))

    if ok: # limpar arquivo
        open("log/reviews.csv", mode="w+").close()
