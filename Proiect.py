import pygame 
import os
from glob import glob
import time
import speech_recognition as sr
from random import shuffle
from playsound import playsound
import datetime
import pywhatkit as kit
import wikipedia
import pyttsx3

inregistrare = sr.Recognizer()

def inregistrare_audio(caută=False):
    with sr.Microphone() as microfon:
        if caută:
            voce_bot(caută)
        print("Se elimina zgomotul de fundal, va rugam asteptati semnalul sonor!")
        inregistrare.adjust_for_ambient_noise(microfon, duration=1)
        playsound("Start.wav")
        voce_inregistrata = ''
        try:
            date_audio = inregistrare.listen(microfon, 10, 10)
            voce_inregistrata = inregistrare.recognize_google(date_audio, language='ro-Ro')
            print(voce_inregistrata)
        except sr.UnknownValueError:
            voce_bot('Scuze, nu am înțeles!')
        except sr.RequestError:
            voce_bot('Momentan indisponibil!')
        return voce_inregistrata

def inregistrare_joc():
    with sr.Microphone() as microfon:
        print('\nCare este tara?')
        audio = inregistrare.record(microfon, duration=5)
    try:
        text = inregistrare.recognize_google(audio, language='ro-RO')
        print(text)
    except sr.UnknownValueError:
        print('')
        text = ''
    except sr.RequestError:
        print('Momentan indisponibil!')
    return text

def voce_bot(mesaj_scris):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate',130)
    engine.say(mesaj_scris)
    print(mesaj_scris)
    engine.runAndWait()

def locatie(locatie_steag):
    fereastra_joc = pygame.display.set_mode((400, 500))
    steaguri_loc = [x for x in glob(locatie_steag + "\\*.PNG")]
    numele = [x.split(".")[0] for x in glob(locatie_steag + "\\*.PNG")]
    steaguri = {k: v for k, v in zip(steaguri_loc, numele)}
    cuvinte = list(steaguri.keys())
    shuffle(cuvinte)
    nr_cuvinte = len(cuvinte)
    punctaj = 0
    for steag in cuvinte:
        fereastra_joc.fill((220, 220, 220))
        imagine = pygame.image.load(os.path.join('', steag))
        fereastra_joc.blit(imagine, (50, 50))
        pygame.display.update()
        if inregistrare_joc() == steaguri[steag].split("\\")[1]:
            voce_bot('Foarte bine!\n---------------------\n\n')
            punctaj += 1
        else:
            voce_bot("Raspuns gresit!")
            print("Raspuns corect:", steaguri[steag].split("\\")[1])
        print(f"Scorul tău este: {punctaj}/{nr_cuvinte}" )
    voce_bot(f"Scorul tău este: {punctaj} din {nr_cuvinte}" )

def countdown(secunde):
    while secunde>0:
        print(secunde)
        secunde -= 1
        time.sleep(1)
        
    t = 0
    while t < 3: 
        playsound('ding.wav')
        t += 1

def set_coutdown():
    minute = inregistrare_audio('Câte minute?')
    if 'zero' in minute :
        minute = 0
    elif 'unu' in minute:
        minute = 1
    elif 'două' in minute:
        minute = 2
    elif 'trei' in minute:
        minute = 3
    elif 'patru' in minute:
        minute = 4
    elif 'cinci' in minute:
        minute = 5
    elif 'șase' in minute:
        minute = 6
    elif 'șapte' in minute:
        minute = 7
    elif 'opt' in minute:
        minute = 8
    elif 'nouă' in minute:
        minute = 9
    if int(minute) > 0:
        minute = int(minute)
        minute = int(minute/0.0166667 + 1)
        print(minute)
    else:
        minute = 0
    secunde = inregistrare_audio('Câte secunde?')
    if 'zero' in secunde :
        secunde = 0
    elif 'unu' in secunde:
        secunde = 1
    elif 'două' in secunde:
        secunde = 2
    elif 'trei' in secunde:
        secunde = 3
    elif 'patru' in secunde:
        secunde = 4
    elif 'cinci' in secunde:
        secunde = 5
    elif 'șase' in secunde:
        secunde = 6
    elif 'șapte' in secunde:
        secunde = 7
    elif 'opt' in secunde:
        secunde = 8
    elif 'nouă' in secunde:
        secunde = 9
    secunde = int(secunde)
    secunde_totale = minute + secunde
    voce_bot(f'Timpul setat este de {int(minute/60)} minute și {secunde} secunde')
    return secunde_totale

def raspunsuri(voce_inregistrata):
    if  str.lower(voce_inregistrata) == 'cât este ceasul' or str.lower(voce_inregistrata) == 'ce oră este':
        timp = datetime.datetime.fromtimestamp(os.path.getmtime(__file__))
        voce_bot(timp.strftime("%H:%M"))
    
    if  str.lower(voce_inregistrata) == 'în ce zi suntem' or str.lower(voce_inregistrata) == 'ce dată este astăzi':
        timp = datetime.datetime.fromtimestamp(os.path.getmtime(__file__))
        voce_bot(timp.strftime("%d %m %Y"))

    if 'caută' in str.lower(voce_inregistrata):
        caută = inregistrare_audio('Ce vrei să caut?')
        kit.search(f"{caută}")

    if 'muzică' in str.lower(voce_inregistrata):
        muzica = inregistrare_audio('Ce melodie?')
        kit.playonyt(f"{muzica}")

    if 'informații' in str.lower(voce_inregistrata):
        wikipedia.set_lang("ro")
        try:
            subiect = inregistrare_audio("Ce subiect?")
            voce_bot(wikipedia.summary(subiect,sentences = 1))
        except:
            voce_bot("Scuze, nu am găsit rezultate pentru acest subiect!")

    if 'vreau să mă joc' in str.lower(voce_inregistrata):
        joc = inregistrare_audio('Ce joc?\n Alege din următoarele jocuri: \n1.Ghicește steagul \n2.Ghicește numărul')
        if joc == 'Ghicește steagul':
            locatie_steag = inregistrare_audio('Steaguri din regiunea:\n 1.Europa \n 2.America de Nord \n 3.America de Sud')
            while locatie_steag == 'Europa':
                locatie(locatie_steag)
                break
            while locatie_steag == 'America de Nord':
                locatie(locatie_steag)
                break    
            while locatie_steag == 'America de Sud':
                locatie(locatie_steag)
                break
    
    if 'cronometru' in str.lower(voce_inregistrata):
        secunde_totale = set_coutdown()
        cronometru = secunde_totale
        countdown(cronometru)


time.sleep(1)
voce_bot('Cu ce te pot ajuta?')
voce_inregistrata = inregistrare_audio()
raspunsuri(voce_inregistrata)
