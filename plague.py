#! /usr/bin/env python3

#___________________________________________Nongma SORGHO___________________________________________#
#Ceci est une implémentation de ce qui pourrait être l'algorithme à la base du jeu Plague Inc.

"""
Plague Inc. est un jeu dans lequel la population mondiale évolue en fonction de certaines variables de maladie.
Je réaliserai cette expérience pour une maladie bactérienne dont les paramètres symptomatique, de transmission et
de létalité posséderont 3 niveaux de dangérosité.
Je prendrai une population mondiale à 7 milliards en supposant que 20% des individus appliquent les règles élémentaires
d'hygiène, ce qui entravera quelque peu l'évolution de la maladie si elle se trouve en des niveaux peu élevés.
Un autre facteur empêchant, et pouvant même stopper la propagation de la maladie et qui sera pris en compte par cet
algorithme est la recherche qui est menée sur le plan international et qui aboutit après 5 minutes de jeu en temps réel.
En début de jeu, le joueur dispose d'un crédit qui lui permettra de faire les améliorations génétiques sur sa maladie.
Par ailleurs, ce crédit augmentera de 95 unités chaque seconde. Il devra donc faire une efficiente utilisation de son
crédit pour atteindre la victoire ! Il existe des mots bonus rapportant une certaine quantité de crédits mais qui
ne pourront être tapés en une seconde que par les plus rapides des joueurs. Alors, seuls les plus expérimentés des joueurs
pourront espérer gagner le niveau difficile.
Pour les symptomes :
- Niv.1 : 113803 morts/sec  Prix : 1000 crédits
- Niv.2 : 2*113803 morts/sec  Prix : 2000 crédits
- Niv.3 : 3*113803 morts/sec  Prix : 3000 crédits
Pour la transmitivité : #Notez que les dégâts infligés par une transmissivité plus grande évolueront de manière exponentielle, ces valeurs sont donc données à titre indicatif
- Niv.1 : + 20% de victimes en plus   Prix : 2000 crédits
- Niv.2 : + 40% de victimes en plus  Prix : 4000 crédits
- Niv.3 : + 60% de victimes en plus  Prix : 8000 crédits
Pour la létalité :
- Niv.1 : 250520 morts/sec   Prix : 1500 crédits
- Niv.2 : 2*250520 morts/sec   Prix : 3000 crédits
- Niv.3 : 3*250520 morts/sec   Prix : 5000 crédits
"""

import time
import signal
import os
import random

population = 7000000000
recherche = 0
credit = 2500
niveau_symptome = 0
niveau_transmissivite = 0
niveau_letalite = 0
symptome = 113803
transmissivite = 0.2
letalite = 250520
compteur = 0

def routine_principale() :
    print("                       Bienvenue sur Plague Inc. by Gerard!\n")
    time.sleep(3)
    for i in range(3 , 0, -1) :
        if i == 1 :
            print("                  Une nouvelle partie débutera dans", i, "seconde\n")
            time.sleep(1)
            os.system('cls')
        else :
            print("                  Une nouvelle partie débutera dans", i, "secondes\n")
            time.sleep(1)
            os.system('cls')
    reponse = str(input(" Bienvenue sur la version minimaliste, si on puisse se le permettre, de Plague Inc.\n Touchez 'C' pour commencer la partie\n"
          " Vous trouverez les instructions et l'aide de jeu en appuyant sur 'A'\n Appuyez sur 'Q' pour quitter la partie\n"))
    if reponse == "C" or reponse == "c" :
        dif = str(input(" Vous avez le choix entre trois (03) niveaux de difficulté : 'F' pour Facile, 'M' pour moyen et 'D' pour Difficile.\n  Veuillez choisir s'il vous plait !\n"))
        if dif == "F" or dif == "f" :
            return maladie(population, recherche, credit, symptome,
            niveau_symptome, transmissivite, niveau_transmissivite, letalite, niveau_letalite, compteur, 1)
        if dif == "M" or dif == "m" :
            return maladie(population, recherche, credit, symptome,
                           niveau_symptome, transmissivite, niveau_transmissivite, letalite, niveau_letalite, compteur,
                           0.5)
        if dif == "D" or dif == "d" :
            return maladie(population, recherche, credit, symptome,
                           niveau_symptome, transmissivite, niveau_transmissivite, letalite, niveau_letalite, compteur,
                           0.2)
    if reponse == "A" or reponse == "a" :
        print("Vous disposerez d'une seconde pour chaque instruction que vous taperez\n"
            "Pour les symptomes : 'S'\n"
              "- Niv.1 : 113803 morts/sec  Prix : 1000 crédits\n"
              "- Niv.2 : 2*113803 morts/sec  Prix : 2000 crédits\n"
              "- Niv.3 : 3*113803 morts/sec  Prix : 3000 crédits\n"
              "Pour la transmitivité : 'T'\n#Notez que les dégâts infligés par une transmissivité plus grande évolueront de manière exponentielle, ces valeurs sont donc données à titre indicatif\n"
              "- Niv.1 : + 20% de victimes en plus   Prix : 2000 crédits\n"
              "- Niv.2 : + 40% de victimes en plus  Prix : 4000 crédits\n"
              "- Niv.3 : + 60% de victimes en plus  Prix : 8000 crédits\n"
              "Pour la létalité : 'L'\n"
              "- Niv.1 : 250520 morts/sec   Prix : 1500 crédits\n"
              "- Niv.2 : 2*250520 morts/sec   Prix : 3000 crédits\n"
              "- Niv.3 : 3*250520 morts/sec   Prix : 5000 crédits\n"
              "#Vous aurez 200 crédits en tapant 'cadeau'\n#Vous aurez 500 crédits en tapant 'chanceux' avec une chance de 75%\n#Vous aurez 100 crédits en tapant 'cent\n"
              "Appuyez 'R' pour retourner au jeu et 'Q' pour quitter\n")
        a = str(input())
        if a == 'R' or a == 'r' :
            return routine_principale()
        else :
            return
    if reponse == "Q" :
        return

total = 0
def maladie(population, recherche, credit, symptome,
            niveau_symptome, transmissivite, niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte) :
    global total
    total += credit
    couleurs = ['echo "\033[30m                              Plague Inc., par Gérard!\033[00m"', 'echo "\033[31m                              Plague Inc., par Gérard!\033[00m"', 'echo "\033[32m                              Plague Inc., par Gérard!\033[00m"',
                                                                                                                                                                                  'echo "\033[33m                              Plague Inc., par Gérard!\033[00m"',
                'echo "\033[34m                              Plague Inc., par Gérard!\033[00m"', 'echo "\033[35m                              Plague Inc., par Gérard!\033[00m"',
                'echo "\033[36m                              Plague Inc., par Gérard!\033[00m"', 'echo "\033[37m                              Plague Inc., par Gérard!\033[00m"']
    os.system(couleurs[random.randint(0,7)])
    print("Avancée de la recherche :", int(recherche), "%\n\n"+" Population :", int(population), "           Morts :", int(7e9-population), "\n\n"+" Crédit :", credit, "\n\n"
                                                                                                   " Niveaux :",
          "Gène S: Niv." + str(niveau_symptome)+" | ", "Gène T: Niv." + str(niveau_transmissivite)+" | ",
          "Gène L: Niv." + str(niveau_letalite)+" \n")
    action = str(entree("#Instructions pour les passages de niveaux des paramètres de votre maladie :\n#Vous taperez 'S' pour Symptome, 'T' pour transmissivité, "
                   "'L' pour létalité\n#Vous aurez 200 crédits en tapant 'cadeau'\n#Vous aurez 500 crédits en tapant 'chanceux' avec une chance de 75%\n#Vous aurez 100 crédits en tapant 'cent'\n\n"))
    if population <= 0.0 :
        score = total + 20000/recherche
        print("Avancée de la recherce :", recherche, "%\n\n Population : 0", "\n\n Crédit :", credit, "\n\n"
                                                                                                                 "Niveaux :",
              "Gène S: Niv."+str(niveau_symptome)+"  ", "Gène T: Niv."+str(niveau_transmissivite)+"  ", "Gène L: Niv."+str(niveau_letalite)+" \n\n")
        print("$$$$$Vous avez gagné, votre maladie a exterminé la population mondiale!$$$$$\n"
              "Votre score est de", score)
        rejouer = str(input("*Souhaitez-vous rejouer ? (Répondez par 'O' pour Oui et 'N' pour Non)*\n"))
        if rejouer == 'O' or rejouer == 'o' :
            return routine_principale()
        else :
            print("*A bientôt pour une nouvelle partie de Plague Inc.*")
            return
    if recherche >= 100 :
        score = total + 20000 / recherche
        print(" Avancée de la recherce : 100", "%\n\n Population :", population, "\n\n Crédit :", credit, "\n\n"
                                                                                                       "Niveaux :",
              "Gène S: Niv." + str(niveau_symptome) + "  ", "Gène T: Niv." + str(niveau_transmissivite) + "  ",
              "Gène L: Niv." + str(niveau_letalite) + " \n\n")
        print("____Vous avez échoué, un remède a été trouvé à votre maladie !____\n"
              "Votre score est de", score)
        rejouer = str(input("*Souhaitez-vous rejouer ? (Répondez par 'O' pour Oui et 'N' pour Non)*\n"))
        if rejouer == 'O':
            return routine_principale()
        else:
            print("*A bientôt pour une nouvelle partie de Plague Inc.*")
            return
    else :
        os.system('cls')
        compteur += difficulte
        if recherche >= 80 :
            recherche += 0.54
        if recherche < 80 :
            recherche += 0.36
        credit += 95
        population -= (symptome * niveau_symptome + letalite * niveau_letalite) + (symptome * niveau_symptome + letalite * niveau_letalite) * transmissivite * niveau_transmissivite * compteur
        if action == "cheat" or action == "CHEAT" or action == "tri" or action == "TRI" :
            population -= 1000000000
        if action == 'chanceux' or action == 'CHANCEUX' :
            if random.random() >= 0.75 :
                credit += 500
        if action == "cadeau" or action == "CADEAU" :
            credit += 200
        if action == "cent" or action == "CENT" :
            credit += 100
        if (action == "S" or action == 's') and niveau_symptome <= 2 :
            if niveau_symptome == 0 and credit >= 1000:
                credit -= 1000
                niveau_symptome += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_symptome == 0 and credit < 1000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_symptome == 1 and credit >=2000 :
                credit -= 2000
                niveau_symptome += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_symptome == 1 and credit < 2000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_symptome == 2 and credit >= 3000 :
                credit -= 3000
                niveau_symptome += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_symptome == 2 and credit < 3000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
        if (action == "T" or action == "t") and niveau_transmissivite <= 2 :
            if niveau_transmissivite == 0 and credit >= 2000 :
                credit -= 2000
                niveau_transmissivite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_transmissivite == 1 and credit < 2000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_transmissivite == 1 and credit >= 4000 :
                credit -= 4000
                niveau_transmissivite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_transmissivite == 1 and credit < 4000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_transmissivite == 2 and credit >= 8000 :
                credit -= 8000
                niveau_transmissivite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_transmissivite == 2 and credit < 8000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
        if (action == "L" or action == "l") and niveau_letalite <= 2 :
            if niveau_letalite == 0 and credit >= 1500 :
                credit -= 1500
                niveau_letalite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_letalite == 0 and credit < 1500:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_letalite == 1 and credit >= 3000 :
                credit -= 3000
                niveau_letalite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_letalite == 1 and credit < 3000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_letalite == 2 and credit >= 5000 :
                credit -= 5000
                niveau_letalite += 1
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
            if niveau_letalite == 2 and credit < 5000:
                return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                               niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)
        else :
            return maladie(population, recherche, credit, symptome, niveau_symptome, transmissivite,
                           niveau_transmissivite, letalite, niveau_letalite, compteur, difficulte)

class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

def entree(Prompt='', timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = input(Prompt)
        signal.alarm(0)
        return text
    except AlarmException:
        print ('\nJeu développé par Nongma SORGHO')
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


routine_principale()

