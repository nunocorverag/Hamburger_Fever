import pygame

pygame.init()

#Background
background_menu_image = pygame.image.load("images/game_over_image.jpg")
background_menu_image = pygame.transform.scale(background_menu_image, (1080, 720))

#Continue
continue_button_image = pygame.image.load("images/buttons/continue_btn.png")
continue_button_image = pygame.transform.scale(continue_button_image, (350, 100))

#High Score
high_score_button_image = pygame.image.load("images/buttons/high_score_btn.png")
high_score_button_image = pygame.transform.scale(high_score_button_image, (350, 100))

#Title font
title_font = pygame.font.Font("freesansbold.ttf", 64)

# Font configuration
font = pygame.font.Font("freesansbold.ttf", 36)

def title_text(screen):
    title_text = title_font.render("Game Over", True, (0,0,0))
    screen.blit(title_text, (360, 100))

class OverScreen:

    # Verify if continue button was clicked
    def check_continue_click(mouse_pos):
        continue_button_rect = continue_button_image.get_rect(topleft=(150, 600))
        if continue_button_rect.collidepoint(mouse_pos):
            return True
        return False

    # Verify if high score button was clicked
    def check_high_score_click(mouse_pos):
        high_score_button_rect = high_score_button_image.get_rect(topleft=(550, 600))
        if high_score_button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        title_text(self.screen)
        self.screen.blit(continue_button_image, (150,600))
        self.screen.blit(high_score_button_image, (550,600))
