import pyttsx3

def tts(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english+f3')
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()
