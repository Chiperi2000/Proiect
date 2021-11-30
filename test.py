import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# print(voices[1].id)
engine.setProperty('rate',150)
engine.say("Salut, numele meu este Andrei și sunt asistentul tău virtual!")
engine.runAndWait()