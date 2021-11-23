import pygame
import os
from glob import glob
import time
import speech_recognition as sr
from random import shuffle
from time import ctime, daylight
import webbrowser
from playsound import playsound
import random
from gtts import gTTS

inregistrare = sr.Recognizer()


def inregistrare_audio(caută=False):
    with sr.Microphone() as microfon:
        if caută:
            print(caută)
        print("Se elimina zgomotul de fundal, va rugam asteptati!")
        inregistrare.adjust_for_ambient_noise(microfon, duration=1)
        voce_bot('Cu ce te pot ajuta?')
        voce_inregistrata = ''
        try:
            date_audio = inregistrare.listen(microfon, 10, 3)
            voce_inregistrata = inregistrare.recognize_google(date_audio, language='ro-Ro')
            print(voce_inregistrata)
        except sr.UnknownValueError:
            voce_bot('Scuze, nu am înțeles!')
        except sr.RequestError:
            voce_bot('Momentan indisponibil!')
        return voce_inregistrata

def voce_bot(mesaj_scris):
    text = gTTS(text=mesaj_scris, lang='ro')
    r = random.randint(1, 100000)
    audio_f = 'fisier-' + str(r) + '.mp3'
    text.save(audio_f)
    playsound(audio_f)
    print(mesaj_scris)
    os.remove(audio_f)

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
        if inregistrare_joc() == 'stop':
            pygame.quit()
        else:
            if inregistrare_joc() == steaguri[steag].split("\\")[1]:
                print('Foarte bine!\n---------------------\n\n')
                punctaj += 1
            else:
                print("Raspuns gresit!")
            print(f"Scorul tău este: {punctaj}/{nr_cuvinte}" )


def raspunsuri(voce_inregistrata):
    if 'cine ești tu' in voce_inregistrata:
        voce_bot("Eu sunt asistentul tău personal!")

    if 'Cât este ceasul' in voce_inregistrata:
        print(ctime())

    if 'caută' in voce_inregistrata:
        caută = inregistrare_audio('Ce vrei sa caut?')
        url = 'https://google.ro/search?q=' + caută
        webbrowser.get().open(url)
        print('Rezultate gasite pentru: ' + caută)

    if 'Vreau să mă joc' in voce_inregistrata:
        joc = inregistrare_audio('Ce vrei sa te joci?\n1.Ghicește steagul')
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


voce_inregistrata = inregistrare_audio()
raspunsuri(voce_inregistrata)
  