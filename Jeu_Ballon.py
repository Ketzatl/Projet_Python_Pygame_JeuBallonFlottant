import pygame

blue = (113, 177, 227)   # Valeurs RGB Uniquement !
white = (255, 255, 255)

pygame.init()

surfaceW = 800
surfaceH = 500

surface = pygame.display.set_mode((surfaceW, surfaceH))
pygame.display.set_caption("Ballon Volant")

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    surface.fill(blue)

    pygame.display.update()


pygame.quit()
quit()
