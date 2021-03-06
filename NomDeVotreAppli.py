import pygame
import time
from random import *
import sqlite3


blue = (113, 177, 227)   # Valeurs RGB Uniquement !
white = (255, 255, 255)

pygame.init()
Donnees = "/Users/morgannott/Documents/Dev_app/xX_PYTHON_Projets_GitHub/Projet_JeuBallon_Pygame/BDD_Ballon_Flottant/Donnees.sq3"
conn = sqlite3.connect(Donnees)
cur = conn.cursor()

## -------- Après le 1er lancement du programme, mettre les 5 lignes suivantes en commentaire !

## cur.execute("CREATE TABLE joueurs (score integer)")

## -------- Création d'un fichier (avec 2 valeurs à l'intérieur) pour le 1er lancement uniquement

## cur.execute("INSERT INTO joueurs (score) VALUES (0)")
## conn.commit()

## cur.execute("INSERT INTO joueurs (score) VALUES (0)")
## conn.commit()


# -------------------------------------------------------------------------

surfaceW = 800
surfaceH = 500

ballonW = 50
ballonH = 66

nuageW = 256
nuageH = 256



surface = pygame.display.set_mode((surfaceW, surfaceH))
pygame.display.set_caption("Ballon Volant")
horloge = pygame.time.Clock()


img = pygame.image.load('ballon.png')
img_nuageB = pygame.image.load('nuageHaut.png')
img_nuageH = pygame.image.load('nuageBas.png')

def Hscore(compte):
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("High Score : " + str(compte), True, white)
    surface.blit(texte, [700, 4])

def score(compte):
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("Score : " + str(compte), True, white)
    surface.blit(texte, [10, 4])


def nuages(x_nuage, y_nuage, espace):
    surface.blit(img_nuageH,(x_nuage, y_nuage))
    surface.blit(img_nuageB,(x_nuage, y_nuage + nuageW + espace))

def rejoueOuQuitte():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP:
            continue
        return event.key
    return None

def creaTexteObj(texte, Police):
    texteSurface = Police.render(texte, True, white)
    return texteSurface, texteSurface.get_rect()

def message(texte):
    GOTexte = pygame.font.Font('BradBunR.ttf',150)
    petitTexte = pygame.font.Font('BradBunR.ttf',20)

    GOTexteSurf, GOTexteRect = creaTexteObj(texte, GOTexte)
    GOTexteRect.center = surfaceW / 2, ((surfaceH/2)-44)
    surface.blit(GOTexteSurf, GOTexteRect)

    petitTexteSurf, petitTexteRect = creaTexteObj("Appuyez sur une touche pour continuer !", petitTexte)
    petitTexteRect.center = surfaceW / 2, ((surfaceH / 2) + 44)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()
    time.sleep(2)

    while rejoueOuQuitte() == None:
        horloge.tick()

    principale()

def gameOver(score_actuel):
    a = [str(score_actuel)]

    Donnees = "/Users/morgannott/Documents/Dev_app/xX_PYTHON_Projets_GitHub/Projet_JeuBallon_Pygame/BDD_Ballon_Flottant/Donnees.sq3"
    conn = sqlite3.connect(Donnees)
    cur = conn.cursor()
    cur.execute("SELECT * FROM joueurs")
    liste = list(cur)

    hscore = []
    for i in range(0, len(liste)):
        hscore += liste[i]

    if (int(hscore[-1]) < score_actuel):
        cur.execute("INSERT INTO joueurs(score) VALUES(?)", a)
        conn.commit()
        cur.close()
        conn.close()

    message("Boom!!")


def ballon(x, y, image):
    surface.blit(image, (x, y))   # Superposition du ballon sur le background (.blit)


def principale():
    x = 150
    y = 200
    y_mouvement = 0

    x_nuage = surfaceW
    y_nuage = randint(-230, 30)
    espace = ballonH * 3
    nuage_vitesse = 4

    score_actuel = 0


    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_mouvement = -5
            if event.type == pygame.KEYUP:
                y_mouvement = 5

        y += y_mouvement

        surface.fill(blue)
        ballon(x, y, img)

        nuages(x_nuage, y_nuage, espace)

        score(score_actuel)

        cur.execute("SELECT * FROM joueurs")
        liste = list(cur)
        print(cur)
        print(liste)


        hscore = []
        for i in range(0, len(liste)):
            hscore += liste[i]
        print(hscore)

        Hscore(hscore[-1])


        x_nuage -= nuage_vitesse

        if y > surfaceH -40 or y < -10:
            gameOver(score_actuel)

        if 4 <= score_actuel  < 5:
            nuage_vitesse = 8
            espace = ballonH * 2.8

        if 8 <= score_actuel < 13:
            nuage_vitesse = 10
            espace = ballonH * 2.6

        if 18 <= score_actuel < 25:
            nuage_vitesse = 12
            espace = ballonH * 2.4

        if 33 <= score_actuel < 44:
            nuage_vitesse = 15
            espace = ballonH * 2


        if x + ballonW > x_nuage + 40:
            if y < y_nuage + nuageH - 80:
                if x - ballonW < x_nuage + nuageW - 20:
                    gameOver(score_actuel)

        if x + ballonW > x_nuage + 40:
            if y + ballonH > y_nuage + nuageH + espace + 10:
                if x - ballonW < x_nuage + nuageW - 20:
                    gameOver(score_actuel)

        if x_nuage < (-1 * nuageW):             # Répétition des nuages, une fois le précédent sorti del'écran
            x_nuage = surfaceW
            y_nuage = randint(-230, 30)         # Repop aléatoire des nuages

        if x_nuage < (x - nuageW) < x_nuage + nuage_vitesse:
            score_actuel += 1

        pygame.display.update()

principale()
pygame.quit()
quit()
