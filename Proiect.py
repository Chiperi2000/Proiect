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
exceptie = ' '

def inregistrare_audio(caută=False):
    with sr.Microphone() as microfon:
        if caută:
            voce_bot(caută)
        print("Se elimina zgomotul de fundal, va rugam asteptati semnalul sonor!")
        inregistrare.adjust_for_ambient_noise(microfon, duration=1)
        playsound("Start.wav")
        voce_inregistrata = ''
        global exceptie
        try:
            date_audio = inregistrare.listen(microfon,phrase_time_limit=5)
            voce_inregistrata = inregistrare.recognize_google(date_audio, language='ro-Ro')
            print(voce_inregistrata)
            exceptie = '0'
        except sr.UnknownValueError:
            voce_bot('Scuze, nu am înțeles!')
            exceptie = '1'
        except sr.RequestError:
            voce_bot('Momentan indisponibil!')
        return voce_inregistrata

def inregistrare_joc():
    with sr.Microphone() as microfon:
        voce_bot('\nCare este țara?')
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
    voce_bot('Stabilire timpi temporizator:')
    minute = inregistrare_audio('Câte minute?')
    while True:
        try:
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
            int(minute)
            break
        except ValueError:
            voce_bot("Te rog să introduci un număr valid!")
            minute = inregistrare_audio('Încearcă din nou! Câte minute?')
    if int(minute) > 0:
        minute = int(minute)
        minute = int(minute/0.0166667 + 1)
    else:
        minute = 0
    secunde = inregistrare_audio('Câte secunde?')
    while True:
        try:
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
            int(secunde)
            break
        except ValueError:
            voce_bot("Te rog să introduci un număr valid!")
            secunde = inregistrare_audio('Incearcă din nou! Câte secunde?')
    secunde = int(secunde)
    secunde_totale = minute + secunde
    voce_bot(f'Timpul setat este de {int(minute/60)} minute și {secunde} secunde')
    voce_bot('Începe cronometrarea!')
    return secunde_totale

def ghiceste_cuvant():
    voce_bot("Bine ai venit la jocul - Ghicește cuvântul!\nTrebuie să îți alegi o categorie din care să facă parte!\n Categorii disponibile:\nBiologie\nInginerie Electrică")
    categorie_aleasa = inregistrare_audio("Spune ce categorie")
    categorii = ['biologie','Inginerie Electrică']
    biologie = ["eucariot","autotrof","tegument","biotrof","oligotrof","hematologie","hipofiza"]
    inginerie_electrica = ["rezistor","condensator","bobina","tensiune","curent"]
    categorie = ''
    validare = ''
    while validare != '1':
        if categorie_aleasa in categorii:
            if 'biologie' in str.lower(categorie_aleasa):
                categorie=biologie
                validare == '1'
                break
            if 'inginerie electrică' in str.lower(categorie_aleasa):
                categorie=inginerie_electrica
                validare == '1'
                break
        else:
            voce_bot("Nu există această categorie! Te rog să încerci din nou!")
            categorie_aleasa = inregistrare_audio("Spune ce categorie")
            validare == "0"
    voce_bot(f'Ai ales categoria {categorie_aleasa}\nMult succes!')
    cuvant_ales = choice(categorie)
    litera_folosita = []
    afisare = cuvant_ales
    for i in range (len(afisare)):
        afisare = afisare[0:i] + "_" + afisare[i+1:]
    incercari = 0
    pygame.init()
    inaltime = latime = 600
    fereastra=pygame.display.set_mode((inaltime,latime))
    pygame.display.set_caption("Spânzurătoarea")
    font_color=(0,150,250)
    font=pygame.font.Font(None,45)
    text=font.render(" ".join(afisare),True,font_color)
    text_incadrare = text.get_rect(center=(latime/2,50))
    imagini = [r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea0.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea1.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea2.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea3.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea4.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea5.png",
    r"D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Spanzuratoarea\Spanzuratoarea6.png"]
    imagine = pygame.image.load(imagini[incercari])
    fereastra.fill((255,255,255))
    fereastra.blit(text,text_incadrare)
    fereastra.blit(imagine,(170,150))
    pygame.display.update()
    print (" ".join(afisare))
    conditie_folosita = '0'
    stop_joc = '0'
    while afisare != cuvant_ales or stop_joc == '1' :
        ghicita = inregistrare_audio("Spune litera: ")
        if 'litera e' in ghicita or 'litera i' in ghicita:
            litera_confirmare = inregistrare_audio("Litera e, și litera i se aseamăna foarte mult în pronunție \n Dacă dorești litera i spune unu \n Dacă dorești litera e spune doi")
            ghicita_conf = ''
            while ghicita_conf != '1':
                if '1' in litera_confirmare or 'unu' in litera_confirmare:
                    ghicita = 'litera i'
                    ghicita_conf = '1'
                elif '2' in litera_confirmare or 'doi' in litera_confirmare:
                    ghicita = 'litera e'
                    ghicita_conf = '1'
                else:
                    voce_bot("Nu este una din variante!")
                    litera_confirmare = inregistrare_audio("Încearcă din nou!")
                    ghicita_conf = '0'
        ghicita = str(ghicita)
        cond_conf_l = ''
        
        while cond_conf_l != '1':
            if 'litera' in ghicita and len(ghicita)<= int('8'):
                litera = ghicita.split().index('litera')
                litera2 = ghicita.split()[litera + 1:]
                cond_conf_l = '1'
                litera_cheie = ' '.join(map(str,litera2))
                ghicita = litera_cheie.lower()
                litera_folosita.extend(ghicita)
                if conditie_folosita == '1':
                    while ghicita in litera_folosita[0:-1]:
                        voce_bot("Litera a fost deja introdusă!")
                        litera_folosita.remove(ghicita)
                        ghicita = inregistrare_audio("Încearcă din nou!Spune litera: ")
                        cond_conf_l = '0'
            else:
                voce_bot("Litera nu este corect introdusă!")
                ghicita = inregistrare_audio("Încearcă din nou!Spune litera: ")
                cond_conf_l = '0'
        numar_incercari = 0
        for i in range(len(cuvant_ales)):
            if cuvant_ales[i] == ghicita:
                afisare = afisare[0:i] + ghicita + afisare[i+1:]
            else:
                numar_incercari = numar_incercari + 1
        if numar_incercari == len(cuvant_ales):
            incercari = incercari + 1
        print("Litere folosite: \n", litera_folosita)
        print(" ".join(afisare))
        conditie_folosita = '1'
        text=font.render(" ".join(afisare),True,font_color)
        litera_folosita_afisare = font.render("  ".join(litera_folosita),True,font_color)
        imagine = pygame.image.load(imagini[incercari])
        fereastra.fill((255,255,255))
        fereastra.blit(text,text_incadrare)
        fereastra.blit(imagine,(170,150))
        fereastra.blit(litera_folosita_afisare,(100,400))
        pygame.display.update()
        if incercari == 6:
            voce_bot("Ai pierdut!")
            voce_bot(f"Cuvântul a fost: {cuvant_ales}")
            break
    if incercari < 6:        
        voce_bot("Foarte bine, ai ghicit!")
        voce_bot(f"Cuvântul a fost: {cuvant_ales}")

def raspunsuri(voce_inregistrata):
    global exceptie
    if  'ceasul' in str.lower(voce_inregistrata)  or 'ora' in str.lower(voce_inregistrata) or 'oră' in str.lower(voce_inregistrata) :
        timp = datetime.datetime.now()
        voce_bot(timp.strftime("%H:%M"))
        return
    
    elif  str.lower(voce_inregistrata) == 'în ce zi suntem' or str.lower(voce_inregistrata) == 'ce dată este astăzi':
        timp = datetime.datetime.now()
        lunile = ["ianuarie","februarie","martie","aprilie","mai","iunie","iulie","august","septembrie","octombire","noiembrie","decembrie"]
        luna =timp.strftime("%m")
        numar_luna = int(luna) - 1
        voce_bot(timp.strftime(f"%d {lunile[numar_luna]} %Y"))
        return

    elif 'google' in str.lower(voce_inregistrata):
        text = voce_inregistrata
        text = str(text)
        cuvant = text.split().index('google')
        cuvant2 = text.split()[cuvant + 1:]
        cuvant_cheie = ' '.join(map(str,cuvant2))
        kit.search(cuvant_cheie)
        return

    elif  'youtube' in str.lower(voce_inregistrata):
        text_yt = voce_inregistrata
        text_yt = str(text_yt)
        cuvant_yt = text_yt.split().index('youtube')
        cuvant2_yt = text_yt.split()[cuvant_yt + 1:]
        cuvant_cheie_yt = ' '.join(map(str,cuvant2_yt))
        kit.playonyt(cuvant_cheie_yt)
        return

    elif 'ce știi despre' in str.lower(voce_inregistrata):
        wikipedia.set_lang("ro")
        text_wk = voce_inregistrata
        text_wk = str(text_wk)
        cuvant_wk = text_wk.split().index('despre')
        cuvant2_wk = text_wk.split()[cuvant_wk + 1:]
        cuvant_cheie_wk = ' '.join(map(str,cuvant2_wk))
        try:
            subiect = cuvant_cheie_wk
            if len(subiect) < int('20'):
                voce_bot(wikipedia.summary(subiect,sentences = 3))
            else:
                voce_bot(wikipedia.summary(subiect,sentences = 1))
        except:
            voce_bot("Scuze, nu am găsit rezultate pentru acest subiect!")

    elif 'vreau să mă joc' in str.lower(voce_inregistrata) or 'joc' in str.lower(voce_inregistrata):
        joc = inregistrare_audio('Alege din următoarele jocuri: \n1.Ghicește steagul; \n2.Ghicește cuvântul;')
        if 'Ghicește steagul' in joc or 'unu' in joc:
            voce_bot("Bine ai venit la jocul - Ghicește steagul! În acest joc trebuie să ghicești steagurile tărilor având ca timp 5 secunde pentru fiecare steag! Alege regiunea de unde dorești steagurile:")
            locatie_steag = inregistrare_audio('\n 1.Europa \n 2.America de Nord \n 3.America de Sud')
            while locatie_steag == 'Europa':
                locatie(locatie_steag)
                pygame.quit()
                return
            while locatie_steag == 'America de Nord':
                locatie(locatie_steag)
                pygame.quit()
                return    
            while locatie_steag == 'America de Sud':
                locatie(locatie_steag)
                pygame.quit()
                return
        elif 'Ghicește cuvântul' in joc or 'doi' in joc:
            ghiceste_cuvant()
            pygame.quit()
            return
        else:
            if exceptie != '1':
                voce_bot(f'Scuze,nu este una din variante! Te rog să încerci din nou!')
            return(raspunsuri('vreau să ma joc'))

    elif 'temporizator' in str.lower(voce_inregistrata) or 'temporizează' in str.lower(voce_inregistrata):
        secunde_totale = set_temporizator()
        cronometru = secunde_totale
        temporizator(cronometru)
        return

    elif 'listă' in str.lower(voce_inregistrata):
        lista()

    elif 'închide calculator' in str.lower(voce_inregistrata):
        os.system('shutdown -s')
    
    else:
        exceptie
        if exceptie != '1':
            voce_bot("Scuze, nu știu această comandă!")

def deschidere_aplicatii(voce_inregistrata):

    if 'chrome' in str.lower(voce_inregistrata) or 'google chrome' in str.lower(voce_inregistrata):
        voce_bot("Se deschide, Google Chrome!")
        os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        return

    elif "excel" in str.lower(voce_inregistrata):
        voce_bot("Se deschide, Microsoft Excel!")
        os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Excel 2010.lnk")
        return

    elif "word" in str.lower(voce_inregistrata):
        voce_bot("Se deschide, Microsoft Word!")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk')
        return
    
    elif 'camera' in str.lower(voce_inregistrata):
        voce_bot("Se deschide camera!")
        os.system('start explorer shell:appsfolder\Microsoft.WindowsCamera_8wekyb3d8bbwe!App')    
        return
    else:
        voce_bot("Aplicația nu este disponibilă!")
def lista():
    adresa = 'D:\Documente\Facultate\Anul 3\Programare Python\Proiect\Liste'
    nume_lista = inregistrare_audio("Denumire listă")
    nume_complet = os.path.join(adresa, nume_lista +".txt") 
    f = open(nume_complet,"w",encoding="utf-8")
    for i in range(1,100000):
        ingrediente = inregistrare_audio(f'{i}')
        if 'listă finalizată' in ingrediente  or 'gata' in ingrediente:
            break
        else:
            nume_l = (f"{i}: {ingrediente} \n")
            f.write(nume_l)
    f.close()
    voce_bot("Lista a fost generată cu succes!")

nume = ' '
def prezentare():
    ora = datetime.datetime.now().hour
    voce_bot("Salut!Eu sunt Andrei, asistentul tău virtual. \nNumele tău care este?")
    global nume
    nume = inregistrare_audio()
    if (ora >= 6) and (ora < 12):
        voce_bot(f"Bună dimineața,{nume}!")
    elif (ora >= 12) and (ora < 18):
        voce_bot(f"Bună ziua,{nume}!")
    elif (ora >= 18) and (ora < 24):
        voce_bot(f"Bună seara,{nume}!")
    start1()

def start1():
    while(1):
        formulari = ["Ce pot face pentru tine?","Cu ce te pot ajuta?"]
        voce_bot(choice(formulari))
        voce_inregistrata = inregistrare_audio().lower()
        if 'deschide' in str.lower(voce_inregistrata):
            deschidere_aplicatii(voce_inregistrata)

        elif 'gata' in str.lower(voce_inregistrata):
            voce_bot(f"La revedere,{nume}")
            break
        else:
            raspunsuri(voce_inregistrata)   
        start2()

def start2():
    cuvant_cheie = ' '
    while 'hei' not in cuvant_cheie:
        with sr.Microphone() as microfon:
            try:
                date_audio = inregistrare.listen(microfon)
                cuvant_cheie = inregistrare.recognize_google(date_audio, language='ro-Ro')
            except sr.UnknownValueError:
                continue
prezentare()