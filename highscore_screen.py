import pygame

pygame.init()

#Background
background_over_image = pygame.image.load("images/menu_screen_background.png")
background_menu_image = pygame.transform.scale(background_over_image, (1080, 720))

#Continue
continue_button_image = pygame.image.load("images/buttons/continue_btn.png")
continue_button_image = pygame.transform.scale(continue_button_image, (350, 100))

#Title font
title_font = pygame.font.Font("freesansbold.ttf", 64)

# Font configuration
font = pygame.font.Font("freesansbold.ttf", 36)

def title_text(screen):
    title_text = title_font.render("Hamburger Fever", True, (255,255,255))
    screen.blit(title_text, (250, 150))

class HighScoreScreen:

    def __init__(self, screen):
        self.screen = screen
        
    # Verify if the return button was clicked
    def check_return_click(mouse_pos):
        return_button_rect = return_button_image.get_rect(topleft=(210, 450))
        if return_button_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        title_text(self.screen)
        self.screen.blit(return_button_image, (610,450))
