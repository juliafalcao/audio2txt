# audio2txt

Um bot Telegram que recebe mensagens de voz e responde com uma transcrição do áudio.

### Tecnologias
- Python 3.7.5
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [speech_recognition](https://pypi.org/project/SpeechRecognition/) (via Google Speech Recognition)
- [ffmpeg](https://ffmpeg.org/)

### Agradecimentos
Bot feito utilizando o wrapper [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot), com base nos exemplos `echobot.py` e `inlinekeyboard.py`. Além disso, [narbehaj/telegram-audio-download](https://github.com/narbehaj/telegram-audio-download/blob/master/tg_audio.py) foi usado como referência para acessar os áudios recebidos.

Para deploy no Heroku, foi utilizado o buildpack [heroku-buildpack-ffmpeg-latest](https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest) para instalação do FFmpeg.
