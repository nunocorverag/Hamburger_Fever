import pygame
import sys

pygame.init()

#Background
background_menu_image = pygame.image.load("images/menu_screen_background.png")
background_menu_image = pygame.transform.scale(background_menu_image, (1080, 720))

#Start
start_button_image = pygame.image.load("images/buttons/start_btn.jpeg")

#Exit
exit_button_image = pygame.image.load("images/buttons/exit_btn.jpeg")

#Title font
title_font = pygame.font.Font("freesansbold.ttf", 64)

#Hamburger image
hamburger_image = pygame.image.load("images/food/hamburger.png")
hamburger_image = pygame.transform.scale(hamburger_image, (200, 200))

# Font configuration
font = pygame.font.Font("freesansbold.ttf", 36)

def title_text(screen):
    title_text = title_font.render("Hamburger Fever", True, (255,255,255))
    screen.blit(title_text, (250, 150))

class MenuScreen:

    # Función para verificar si se hizo clic en el botón de inicio
    def check_start_click(mouse_pos):
        start_button_rect = start_button_image.get_rect(topleft=(210, 450))
        if start_button_rect.collidepoint(mouse_pos):
            return True
        return False

    # Función para verificar si se hizo clic en el botón de salida
    def check_exit_click(mouse_pos):
        exit_button_rect = exit_button_image.get_rect(topleft=(610, 450))
        if exit_button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        self.screen.blit(hamburger_image, (440,220))
        title_text(self.screen)
        self.screen.blit(start_button_image, (210,450))
        self.screen.blit(exit_button_image, (610,450))
