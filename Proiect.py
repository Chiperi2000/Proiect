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

def inregistrare_audio(caută=False):
    with sr.Microphone() as microfon:
        if caută:
            voce_bot(caută)
        print("Se elimina zgomotul de fundal, va rugam asteptati semnalul sonor!")
        inregistrare.adjust_for_ambient_noise(microfon, duration=1)
        playsound("Start.wav")
        voce_inregistrata = ''
        try:
            date_audio = inregistrare.listen(microfon,phrase_time_limit=5)
            voce_inregistrata = inregistrare.recognize_google(date_audio, language='ro-Ro')
            print(voce_inregistrata)
        except sr.UnknownValueError:
            voce_bot('Scuze, nu am înțeles!')
        except sr.RequestError:
            voce_bot('Momentan indisponibil!')
        return voce_inregistrata

def inregistrare_joc():
    with sr.Microphone() as microfon:
        voce_bot('\nCare este tara?')
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
    voce = engine.getProperty('voices')
    engine.setProperty('voice', voce[1].id)
    engine.setProperty('rate',150)
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
            voce_bot("Răspuns greșit!")
            print("Răspuns corect:", steaguri[steag].split("\\")[1])
        print(f"Scorul tău este: {punctaj}/{nr_cuvinte}" )
    voce_bot(f"Scorul tău este: {punctaj} din {nr_cuvinte}" )

def temporizator(secunde):
    while secunde>0:
        print(secunde)
        secunde -= 1
        time.sleep(1)
        
    t = 0
    while t < 3: 
        playsound('ding.wav')
        t += 1

def set_temporizator():
    voce_bot('Stabilire timpi:')
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
    voce_bot('Începe cronometrarea!')
    return secunde_totale

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

def raspunsuri(voce_inregistrata):
    if  'ceasul' in str.lower(voce_inregistrata)  or 'ora' in str.lower(voce_inregistrata) or 'oră' in str.lower(voce_inregistrata) :
        timp = datetime.datetime.fromtimestamp(os.path.getmtime(__file__))
        voce_bot(timp.strftime("%H:%M"))
    
    if  str.lower(voce_inregistrata) == 'în ce zi suntem' or str.lower(voce_inregistrata) == 'ce dată este astăzi':
        timp = datetime.datetime.fromtimestamp(os.path.getmtime(__file__))
        voce_bot(timp.strftime("%d %m %Y"))

    if 'google' in str.lower(voce_inregistrata):
        text = voce_inregistrata
        text = str(text)
        cuvant = text.split().index('google')
        cuvant2 = text.split()[cuvant + 1:]
        cuvant_cheie = ' '.join(map(str,cuvant2))
        kit.search(cuvant_cheie)

    if  'youtube' in str.lower(voce_inregistrata):
        text_yt = voce_inregistrata
        text_yt = str(text_yt)
        cuvant_yt = text_yt.split().index('youtube')
        cuvant2_yt = text_yt.split()[cuvant_yt + 1:]
        cuvant_cheie_yt = ' '.join(map(str,cuvant2_yt))
        kit.playonyt(cuvant_cheie_yt)

    if 'informații' in str.lower(voce_inregistrata) or 'wikipedia' in str.lower(voce_inregistrata) :
        wikipedia.set_lang("ro")
        try:
            subiect = inregistrare_audio("Ce subiect?")
            voce_bot(wikipedia.summary(subiect,sentences = 1))
        except:
            voce_bot("Scuze, nu am găsit rezultate pentru acest subiect!")

    if 'vreau să mă joc' in str.lower(voce_inregistrata) or 'joc' in str.lower(voce_inregistrata):
        joc = inregistrare_audio('Alege din următoarele jocuri: \n1.Ghicește steagul; \n2.Ghicește cuvântul;')
        if 'Ghicește steagul' in joc or 'unu' in joc:
            voce_bot("Bine ai venit la jocul - Ghicește steagul! În acest joc trebuie să ghicești stagurile tărilor având ca timp 5 secunde pentru fiecare steag! Alege regiunea de unde dorești steagurile:")
            locatie_steag = inregistrare_audio('\n 1.Europa \n 2.America de Nord \n 3.America de Sud')
            while locatie_steag == 'Europa':
                locatie(locatie_steag)
                quit()
            while locatie_steag == 'America de Nord':
                locatie(locatie_steag)
                quit()    
            while locatie_steag == 'America de Sud':
                locatie(locatie_steag)
                quit()
        if 'Ghicește cuvântul' in joc or 'doi' in joc:
            ghiceste_cuvant()

    if 'temporizator' in str.lower(voce_inregistrata):
        secunde_totale = set_temporizator()
        cronometru = secunde_totale
        temporizator(cronometru)

    if 'listă' in str.lower(voce_inregistrata):
        lista()

def deschidere_aplicatii(voce_inregistrata):

    if 'chrome' in str.lower(voce_inregistrata) or 'google chrome' in str.lower(voce_inregistrata):
        voce_bot("Se deschide, Google Chrome!")
        os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        return

    elif "word" in str.lower(voce_inregistrata):
        voce_bot("Se deschide, Microsoft Word!")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk')
        return
    
    elif 'camera' in str.lower(voce_inregistrata):
        voce_bot("Se deschide camera!")
        os.system('start explorer shell:appsfolder\Microsoft.WindowsCamera_8wekyb3d8bbwe!App')    
    else:
        voce_bot("Aplicația nu este disponibilă!")
        return
    

def lista():
    adresa = 'D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Liste'
    nume_lista = inregistrare_audio("Denumire listă")
    nume_complet = os.path.join(adresa, nume_lista +".txt") 
    f = open(nume_complet,"w",encoding="utf-8")
    for i in range(1,100000):
        ingrediente = inregistrare_audio(f'{i}')
        if ingrediente != "listă finalizată":
            nume = (f"{i}: {ingrediente} \n")
            f.write(nume)
        else:
            break
    f.close()

if __name__ == "__main__":
    voce_bot("Salut!Eu sunt Andrei, asistentul tău virtual. \nNumele tău care este?")
    nume = inregistrare_audio()
    voce_bot("Salut, " + nume + '.')
      
    while(1):
  
        voce_bot("Ce pot face pentru tine?")
        voce_inregistrata = inregistrare_audio().lower()

        if 'deschide' in str.lower(voce_inregistrata):
            deschidere_aplicatii(voce_inregistrata)
        else:
            raspunsuri(voce_inregistrata)
        
        if voce_inregistrata == 0:
            continue
  
        if "gata" in voce_inregistrata:
            voce_bot("La revedere, "+ nume +'.')
            break
