import speech_recognition as sr


def speeh():
    recognizer = sr.Recognizer()

    ''' recording the sound '''

    with sr.AudioFile("tg_voice.mp3") as source:
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
