import speech_recognition as sr
from pydub import *
from os import path


def speeh():
    recognizer = sr.Recognizer()
    scr = 'tg_voice.mp3'
    out = '/voice/tg_vc.wav'
    sound = AudioSegment.from_mp3(scr)
    sound.export(out, format='wav')
    ''' recording the sound '''

    with sr.AudioFile(r'voice\tg_vc.wav') as source:
        recorded_audio = recognizer.listen(source)

    ''' Recorgnizing the Audio '''
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
            recorded_audio,
            language="ru-RU"
        )
        return "Decoded Text : {}".format(text)

    except Exception as ex:
        print(ex)


speeh()
