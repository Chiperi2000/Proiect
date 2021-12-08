from random import shuffle, choice

biologie = ['mana dreapta']
cuvant_ales = choice(biologie)
print(cuvant_ales)

afisare = cuvant_ales
cuvant_ales2=(len(cuvant_ales) - cuvant_ales.count(' '))

for i in range (len(afisare)):
        afisare = afisare[0:i] + "_" + afisare[i+1:]

print (" ".join(afisare))