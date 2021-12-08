import pygame 
import os
from glob import glob
import time
import speech_recognition as sr
from random import shuffle, choice
from playsound import playsound
import datetime
import pywhatkit as kit
import wikipedia
import pyttsx3

inregistrare = sr.Recognizer()

def voce_bot(mesaj_scris):
    engine = pyttsx3.init()
    voce = engine.getProperty('voices')
    engine.setProperty('voice', voce[1].id)
    engine.setProperty('rate',150)
    engine.say(mesaj_scris)
    print(mesaj_scris)
    engine.runAndWait()

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


def ghiceste_cuvant():
    voce_bot("Bine ai venit la jocul - Ghicește cuvântul!\nTrebuie să îți alegi o categorie din care să facă parte!\n Categorii disponibile:\nBiologie\nInginerie Electrică")
    categorie_aleasa = inregistrare_audio("Spune ce categorie")
    categorii = ['biologie','inginerie electrică']
    biologie = ["eucariot","autotrof","tegmentum","biotrof","oligotrof","hematologie","hipofiza"]
    inginerie_electrica = ["rezistor","condensator","bobina","tensiune","curent",""]
    categorie = ''
    if categorie_aleasa in categorii:
        if categorie_aleasa == 'biologie':
            categorie=biologie
        if categorie_aleasa == 'Inginerie Electrică':
            categorie=inginerie_electrica
    else:
        voce_bot("Nu exsită această categorie!")
        return(ghiceste_cuvant())
    voce_bot(f'Ai ales categoria {categorie_aleasa}\nMult succes!')
    cuvant_ales = choice(categorie)
    print("Cuvantul ales este:", cuvant_ales)
    litera_folosita = []
    afisare = cuvant_ales
    for i in range (len(afisare)):
        afisare = afisare[0:i] + "_" + afisare[i+1:]

    print (" ".join(afisare))
    incercari = 1
    while afisare != cuvant_ales:
        ghicita = inregistrare_audio("Spune litera: ")
        if 'litera e' in ghicita or 'litera i' in ghicita:
            litera_confirmare = inregistrare_audio("Litera e, și litera i se aseamăna foarte mult în pronunție \n Daca dorești litera i spune unu \n Daca dorești litera e spune doi")
            ghicita_conf = '0'
            while ghicita_conf == '0':
                if '1' in litera_confirmare or 'unu' in litera_confirmare:
                    ghicita = 'litera i'
                    ghicita_conf = '1'
                elif '2' in litera_confirmare or 'doi' in litera_confirmare:
                    ghicita = 'litera e'
                    ghicita_conf = '1'
                else:
                    voce_bot("Nu este una din variante!")
        ghicita = str(ghicita)
        litera = ghicita.split().index('litera')
        litera2 = ghicita.split()[litera + 1:]
        litera_cheie = ' '.join(map(str,litera2))
        ghicita = litera_cheie.lower()
        print(ghicita)
        litera_folosita.extend(ghicita)
        print(litera_folosita)
        print ("incercari: ")
        print (incercari)
        for i in range(len(cuvant_ales)):
            if cuvant_ales[i] == ghicita:
                afisare = afisare[0:i] + ghicita + afisare[i+1:]

        print("Litere folosite: \n", litera_folosita)
    
        print(" ".join(afisare))
        incercari = incercari + 1
    voce_bot("Foarte bine, ai ghicit!")
    voce_bot(f"Cuvântul a fost: {cuvant_ales}")

ghiceste_cuvant()