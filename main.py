import pygame
import os
from glob import glob
import time
import speech_recognition as sr
from random import shuffle
from time import ctime, daylight
import webbrowser

inregistrare = sr.Recognizer()

# def inregistrare_audio(caută = False):
#     with sr.Microphone() as microfon:
#         if caută:
#             print(caută)
#         print("Se elimina zgomotul de fundal, va rugam asteptati!")
#         inregistrare.adjust_for_ambient_noise(microfon, duration=1)
#         print('Te ascult...')
#         voce_inregistrata = ''
#         try:
#             date_audio = inregistrare.listen(microfon,10,3)
#             voce_inregistrata = inregistrare.recognize_google(date_audio, language='ro-Ro')
#             print(voce_inregistrata)
#         except sr.UnknownValueError:
#             print('Scuze, nu am inteles!')
#         except sr.RequestError:
#             print('Momentan indisponibil!')
#         return voce_inregistrata



# def raspunsuri(voce_inregistrata):
    
#     if 'Care este numele tău' in voce_inregistrata:
#         print("Numele meu este Mike")
    
#     if 'Cât este ceasul' in voce_inregistrata:
#         print(ctime())
    
#     if 'caută' in voce_inregistrata:
#         caută = inregistrare_audio('Ce vrei sa caut?')
#         url = 'https://google.ro/search?q=' + caută
#         webbrowser.get().open(url)
#         print('Rezultate gasite pentru: ' + caută)
    
#     if 'hai să ne jucăm' in voce_inregistrata:
#         joc = inregistrare_audio('Ce vrei sa ne jucam?')
#         print(joc)
#         if joc == 'Ghicește steagul':
#             fereastra_joc = pygame.display.set_mode((400, 400))
#             steaguri_loc = [x for x in glob("animals\\*.PNG")]
#             numele = [x.split(".")[0] for x in glob("animals\\*.PNG")]
#             steaguri = {k:v for k, v in zip(steaguri_loc, numele)}
#             print(steaguri)
#             print(steaguri_loc)
#             print(numele)
#             cuvinte = list(steaguri.keys())
#             shuffle(cuvinte)
#             score = 0
#             for steag in cuvinte:
#                 guess_counter = 0
#                 carImg = pygame.image.load(os.path.join('', steag))
#                 fereastra_joc.blit(carImg,(130,0))
#                 pygame.display.update()
#                 r = sr.Recognizer()
#                 with sr.Microphone() as source:
#                     print ('What\'s his name!')
#                     audio = r.listen(source)
#                 try:
#                     text = r.recognize_google(audio)
#                     print(text)
#                 except:
#                     print('Did not get that try Again')
#                     text=''
#                 if text == steaguri[steag].split("\\")[1]:
#                     print('good job\n=========\n\n') 
#                     score += 1
#                 else:
#                     if guess_counter < 3:
#                         print('wrong try again\n')
#                         guess_counter += 1
#                     else:
#                         pygame.quit()
#                 fereastra_joc.fill((0,0,0))
#                 print(f"{score}") 
#             pygame.quit()  


# voce_inregistrata = inregistrare_audio()
# raspunsuri(voce_inregistrata)


fereastra_joc = pygame.display.set_mode((400, 500))
steaguri_loc = [x for x in glob("Europa\\*.PNG")]
numele = [x.split(".")[0] for x in glob("Europa\\*.PNG")]
steaguri = {k:v for k, v in zip(steaguri_loc, numele)}
cuvinte = list(steaguri.keys())
shuffle(cuvinte)
score = 0
for steag in cuvinte:
    guess_counter = 0
    imagine = pygame.image.load(os.path.join('', steag))
    fereastra_joc.blit(imagine,(50,50))
    pygame.display.update()
    with sr.Microphone() as microfon:
        print ('Care este tara?')
        audio = inregistrare.listen(microfon)
    try:
        text = inregistrare.recognize_google(audio,language='ro-RO')
        print(text)
    except sr.UnknownValueError:
        print('Scuze, nu am inteles!')
        text=''
    if text == steaguri[steag].split("\\")[1]:
        print('Foarte bine!\n---------------------\n\n') 
        score += 1
    elif text == 'stop':
        pygame.quit()
    else:
        if guess_counter < 3:
            print('wrong try again\n')
            guess_counter += 1
        else:
            pygame.quit()
    print(f"Scorul tău este: {score}") 
