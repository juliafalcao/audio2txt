import os
import json
import speech_recognition as sr
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

"""
Wrapper das funções de transcrição
"""
def transcribe(wav_filepath) -> str:
    if os.environ.get("ENGINE", "") == "IBM":
        return transcribe_ibm(wav_filepath)
    else:
        return transcribe_google(wav_filepath)

"""
Função que recebe o path completo de um arquivo .wav e efetua a transcrição usando o reconhecedor do Google.
"""
def transcribe_google(wav_filepath) -> str:
    rec = sr.Recognizer()
    rec.energy_threshold = 300

    rec = sr.Recognizer()
    rec.energy_threshold = 300 
    audiofile = sr.AudioFile(wav_filepath)

    with audiofile as source:
        audio = rec.record(source)

    return rec.recognize_google(audio, language="pt-BR")

"""
Função que recebe o path completo de um arquivo .wav e efetua a transcrição usando o reconhecedor da IBM.
"""
def transcribe_ibm(wav_filepath) -> str:
    authenticator = IAMAuthenticator(os.environ.get("IBM_CLOUD_API_KEY", ""))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.environ.get("IBM_CLOUD_SERVICE_URL", ""))

    with open(wav_filepath, "rb") as audio_file:
        result_json = speech_to_text.recognize(
            audio=audio_file,
            content_type="audio/wav",
            model="pt-BR_BroadbandModel"
        ).get_result()

    results = result_json.get("results", {})
    if len(results) > 1: # TODO
        results = results.sort(key=lambda x: x.get("confidence", 1), reverse=True)

    alternatives = results[0]["alternatives"]
    return alternatives[0]["transcript"]
