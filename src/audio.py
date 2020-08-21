"""
https://github.com/narbehaj/telegram-audio-download/blob/master/tg_audio.py
"""

from requests import get
from random import randint
from json import loads
import os
import subprocess
import logging

from config.bot import bot_token
from src.transcription import transcribe

logger = logging.getLogger()

def get_file_path(file_id):
    get_path = get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    json_doc = loads(get_path.text)
    try:
        file_path = json_doc["result"]["file_path"]
        logging.info("File path: %s" % file_path)
    except Exception as e:  # Happens when the file size is bigger than the API condition
        logging.exception("get_file_path - Exception: %s" % str(e))
        return None

    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

def download_file(file_id, chat_id) -> str:
    download_url = get_file_path(file_id)

    try:
        oga_file = get(download_url)
        logging.info("oga_file: %s" % type(oga_file))
        local_filepath = f"audios/{file_id}.oga"
        with open(local_filepath, "wb") as f:
            f.write(oga_file.content)

        return local_filepath

    except Exception as e:
        logging.info("get_file - Exception: %s" % str(e))
        return None

def convert_to_wav(oga_filepath: str) -> str:
    wav_filepath = oga_filepath.replace(".oga", ".wav")
    logging.info("convert_to_wav - working dir: %s" % os.getcwd())
    process = subprocess.run(["ffmpeg", "-i", oga_filepath, wav_filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.returncode != 0:
        raise Exception("Something went wrong")

    return wav_filepath


def download_and_transcribe(file_id, chat_id):
    # download .oga audio file from chat
    oga_filepath = download_file(file_id, chat_id)

    # convert to .wav
    wav_filepath = convert_to_wav(oga_filepath)

    # process and transcribe
    txt = transcribe(wav_filepath)
    return txt
