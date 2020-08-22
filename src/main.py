#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import os
from src.audio import download_and_transcribe
from src.rating import get_reply_markup, handle_rating_callback

"""
Configurações
"""
bot_token = os.environ.get("BOT_TOKEN", "")
app_url = os.environ.get("APP_URL", "")
PORT = int(os.environ.get("PORT", 5000))

"""
Handler do comando /start
Responde com mensagem de boas vindas
"""
def start(update, context):
    chat_id = update.message.chat.id
    logging.info("[%s] Recebido comando /start" % chat_id)
    emoji = "" # hugging face emoji
    update.message.reply_text("Olá! Seja bem vindo. 🤗 Se você me enviar ou encaminhar uma mensagem de áudio, posso te passar uma transcrição!")

"""
Handler de mensagens de voz/áudio
Responde com transcrição do áudio
"""
def handle_voice_message(update, context):
    chat_id = update.message.chat.id
    file_id = update.message.voice.file_id
    logging.info("[%s] Mensagem de voz recebida", chat_id)

    file_size: int = update.message.voice.file_size
    if file_size > 2_000_000:
        logging.error("[%s] Arquivo maior que 2MB (%sB)", chat_id, file_size)
        update.message.reply_text(f"Sinto muito, só consigo lidar com arquivos menores que <b>2MB</b> 😟", parse_mode="HTML")

    try:
        txt = download_and_transcribe(file_id, chat_id)
        logging.info("[%s] Texto transcrito: %s", chat_id, txt)

        # generate rating keyboard reply markup
        reply_markup = get_reply_markup()

        # reply with transcribed text
        update.message.reply_text(
            f"<b>Transcrição:</b> {txt}",
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        return
    except Exception as e:
        logging.error("[%s] Finalizou com erro: %s", chat_id, str(e))
        err_msg = "Poxa! Não foi possível transcrever esse áudio 😰 Espero que não desista de mim."
        update.message.reply_text(err_msg)

"""
Configuração de logging: um handler para stdout e um para arquivo de log
"""
def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler("audio2txt.log", mode="a+"),
            logging.StreamHandler()
        ]
    )

"""
Função principal que inicia o bot e recebe updates
"""
def main():
    config_logging()
    logging.info("Iniciando bot...")

    # Bot setup
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_rating_callback))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice_message))

    # Run
    logging.info("Bot rodando e aguardando requisições")

    # updater.start_polling() # local

    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=bot_token
    )
    updater.bot.setWebhook(app_url + bot_token)
    updater.idle()
