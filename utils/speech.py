# utils/speech.py
from gtts import gTTS
import os
import playsound
import speech_recognition as sr

accent = os.getenv('ACCENT', 'en')
tld = os.getenv('TLD', 'com')

def speak(text):
    # Google Text-to-Speech
    tts = gTTS(text=text, lang=accent, tld=tld)
    filename = 'temp_voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if isinstance(text, str):
                print("You said: " + text)
                return text
            else:
                print("Unrecognized response type")
                return None
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
