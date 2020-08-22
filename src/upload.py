from time import sleep
import logging
from src.rating import upload_ratings
from src.main import config_logging

if __name__ == "__main__":
    config_logging()
    while True:
        logging.info("[S3] 1h sleep...")
        sleep(60*60) # 1h
        upload_ratings()
