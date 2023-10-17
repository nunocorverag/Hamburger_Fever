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

    def __init__(self, screen):
        self.screen = screen

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
    
    #This function is in testing
    def get_user_name(self):
        input_box = pygame.Rect(540, 300, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((30, 30, 30))
            font = pygame.font.Font(None, 32)
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.display.flip()

        return text

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        title_text(self.screen)
        self.screen.blit(continue_button_image, (150,600))
        self.screen.blit(high_score_button_image, (550,600))
