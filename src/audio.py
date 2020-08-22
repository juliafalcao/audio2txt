"""

"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get
from json import loads
import os
import subprocess
import logging
from tempfile import TemporaryDirectory

from src.transcription import transcribe

bot_token = os.environ.get("BOT_TOKEN", "")

"""
Recebe file_id e chama Telegram API para obter o file_path.
"""
def get_file_path(file_id):
    get_path = get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    json_doc = loads(get_path.text)
    file_path = json_doc["result"]["file_path"]

    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

"""
Recebe path do arquivo de áudio e faz download para um diretório temporário já criado.
Retorna path completo do arquivo baixado (extensão: .oga).
"""
def download_file(file_id, chat_id, temp_dir) -> str:
    logging.info("[%s] Baixando arquivo %s...", chat_id, file_id)
    download_url = get_file_path(file_id)
    oga_file = get(download_url)
    oga_temp = f"{temp_dir}/{file_id}.oga"

    with open(oga_temp, "wb") as f:
        f.write(oga_file.content)

    return oga_temp

"""
Recebe path do arquivo .oga e converte para .wav usando ffmpeg.
Retorna path completo do arquivo .wav gerado.
"""
def convert_to_wav(oga_filepath: str) -> str:
    wav_filepath = oga_filepath.replace(".oga", ".wav")
    process = subprocess.run(["ffmpeg", "-i", oga_filepath, wav_filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.returncode != 0:
        raise Exception("Falha na conversão do .oga para .wav.")

    return wav_filepath

"""
Função principal que recebe um chat_id e um file_id e efetua o download, conversão e transcrição do áudio.
"""
def download_and_transcribe(file_id, chat_id):
    try:
        with TemporaryDirectory() as temp_dir:
            # download .oga audio file from chat
            oga_filepath = download_file(file_id, chat_id, temp_dir)

            # convert to .wav
            wav_filepath = convert_to_wav(oga_filepath)

            # process and transcribe
            txt = transcribe(wav_filepath)
            return txt

    except Exception as e:
        raise e
