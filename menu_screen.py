import pygame
import json

pygame.init()

#Background
background_over_image = pygame.image.load("images/menu_screen_background.png")
background_menu_image = pygame.image.load("images/Fondos/MenuFondo.png")
BIG_background_menu_image = pygame.transform.scale(background_menu_image,(1080,720))

#Start
start_button_image = pygame.image.load("images/buttons/start_btn.jpeg")

#Exit
exit_button_image = pygame.image.load("images/buttons/exit_btn.jpeg")

##button position
button1_pos = (215,550)
button2_pos = (625,550)

#Title font
title_font = pygame.font.Font("freesansbold.ttf", 64)

def get_high_score():
    with open('Hamburger_Fever_Scores.txt', 'r') as file:
        data = json.load(file)
        scores = set(data.values())
        return max(scores)
    
class MenuScreen:

    def __init__(self, screen):
        self.screen = screen
        
    # Verify if start button was clicked
    def check_start_click(mouse_pos):
        start_button_rect = start_button_image.get_rect(topleft=button1_pos)
        if start_button_rect.collidepoint(mouse_pos):
            return True
        return False

    # Verify if exit button was clicked
    def check_exit_click(mouse_pos):
        exit_button_rect = exit_button_image.get_rect(topleft=button2_pos)
        if exit_button_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        self.screen.blit(BIG_background_menu_image, (0,0))
        self.screen.blit(start_button_image, button1_pos)
        self.screen.blit(exit_button_image, button2_pos)
        highest_score = get_high_score()
        text = title_font.render(f'Highest Score: {highest_score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(text, text_rect)
