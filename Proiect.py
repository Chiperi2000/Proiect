import pygame
import os
from glob import glob
import time
import speech_recognition as sr
from random import shuffle
from time import ctime, daylight
import webbrowser

inregistrare = sr.Recognizer()


def inregistrare_audio(caută=False):
    with sr.Microphone() as microfon:
        if caută:
            print(caută)
        print("Se elimina zgomotul de fundal, va rugam asteptati!")
        inregistrare.adjust_for_ambient_noise(microfon, duration=1)
        print('Te ascult...')
        voce_inregistrata = ''
        try:
            date_audio = inregistrare.listen(microfon, 10, 3)
            voce_inregistrata = inregistrare.recognize_google(
                date_audio, language='ro-Ro')
            print(voce_inregistrata)
        except sr.UnknownValueError:
            print('Scuze, nu am inteles!')
        except sr.RequestError:
            print('Momentan indisponibil!')
        return voce_inregistrata


def inregistrare_joc():
    with sr.Microphone() as microfon:
        print('Care este tara?')
        audio = inregistrare.record(microfon, duration=5)
    try:
        text = inregistrare.recognize_google(audio, language='ro-RO')
        print(text)
    except sr.UnknownValueError:
        print('Scuze, nu am inteles!')
        text = ''
    except sr.RequestError:
        print('Momentan indisponibil!')
    return text

def locatie(locatie_steag):
    fereastra_joc = pygame.display.set_mode((400, 500))
    steaguri_loc = [x for x in glob(locatie_steag +"\\*.PNG")]
    numele = [x.split(".")[0] for x in glob(locatie_steag + "\\*.PNG")]
    steaguri = {k: v for k, v in zip(steaguri_loc, numele)}
    cuvinte = list(steaguri.keys())
    shuffle(cuvinte)
    punctaj = 0
    for steag in cuvinte:
        fereastra_joc.fill((220, 220, 220))
        incercari = 0
        imagine = pygame.image.load(os.path.join('', steag))
        fereastra_joc.blit(imagine, (50, 50))
        pygame.display.update()
    if inregistrare_joc() == steaguri[steag].split("\\")[1]:
        print('Foarte bine!\n---------------------\n\n')
        punctaj += 1
    else:
        incercari < 1
        print('Gresit, incearca din nou\n')
        incercari += 1
    if inregistrare_joc() == 'nu mai vreau să joc':
        pygame.quit()
    print(f"Scorul tău este: {punctaj}")


def raspunsuri(voce_inregistrata):
    if 'Care este numele tău' in voce_inregistrata:
        print("Numele meu este ....")

    if 'Cât este ceasul' in voce_inregistrata:
        print(ctime())

    if 'caută' in voce_inregistrata:
        caută = inregistrare_audio('Ce vrei sa caut?')
        url = 'https://google.ro/search?q=' + caută
        webbrowser.get().open(url)
        print('Rezultate gasite pentru: ' + caută)

    if 'hai să ne jucăm' in voce_inregistrata:
        joc = inregistrare_audio('Ce vrei sa te joci?\n 1.Ghicește steagul')
        if joc == 'Ghicește steagul':
            locatie_steag = inregistrare_audio('Steaguri din regiunea:\n 1.Europa \n 2.Asia')
            if locatie_steag == 'Europa':
                locatie(locatie_steag)
            if locatie_steag == 'Asia':
                locatie(locatie_steag)    
                

voce_inregistrata = inregistrare_audio()
raspunsuri(voce_inregistrata)


