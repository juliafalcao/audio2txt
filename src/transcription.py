import speech_recognition as sr

"""
Função que recebe o path completo de um arquivo .wav e efetua a transcrição usando o recognizer do Google.
"""
def transcribe(wav_filepath) -> str:
    rec = sr.Recognizer()
    rec.energy_threshold = 300

    rec = sr.Recognizer()
    rec.energy_threshold = 300 
    audiofile = sr.AudioFile(wav_filepath)

    with audiofile as source:
        audio = rec.record(source)

    return rec.recognize_google(audio, language="pt-BR")
