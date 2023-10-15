import pygame
import math
import random

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((800,600))

#Background
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))

running = True

while running:
    screen.fill((0,0,0))
    screen.blit(background_image, (0,0))

    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #This checks if the key pressed is the left arrow
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4

    #Update the display
    pygame.display.update() 