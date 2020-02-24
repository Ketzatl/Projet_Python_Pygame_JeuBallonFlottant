import pygame
import time
from random import *


blue = (113, 177, 227)   # Valeurs RGB Uniquement !
white = (255, 255, 255)

pygame.init()

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
img_nuageB = pygame.image.load('nuageHaut.gif')
img_nuageH = pygame.image.load('nuageBas.png')

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
    GOTexteRect.center = surfaceW/2, ((surfaceH/2)-44)
    surface.blit(GOTexteSurf, GOTexteRect)

    petitTexteSurf, petitTexteRect = creaTexteObj("Appuyez sur une touche pour continuer !", petitTexte)
    petitTexteRect.center = surfaceW / 2, ((surfaceH / 2) + 44)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()
    time.sleep(2)

    while rejoueOuQuitte() == None:
        horloge.tick()

    principale()

def gameOver():
    message("Boom!!")

def ballon(x, y, image):
    surface.blit(image, (x, y))   # Superposition du ballon sur le background (.blit)


def principale():
    x = 150
    y = 200
    y_mouvement = 0

    x_nuage = surfaceW
    y_nuage = randint(-300, 20)
    espace = ballonH * 3
    nuage_vitesse = 4

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

        x_nuage -= nuage_vitesse

        if y > surfaceH -40 or y < -10:
            gameOver()

        pygame.display.update()

principale()
pygame.quit()
quit()
