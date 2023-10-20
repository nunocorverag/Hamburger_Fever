import pygame

pygame.init()

#Background
background_menu_image = pygame.image.load("images/game_over_image.png")
background_menu_image = pygame.transform.scale(background_menu_image, (1080, 720))

#Continue
continue_button_image = pygame.image.load("images/buttons/continue_btn.png")
continue_button_image = pygame.transform.scale(continue_button_image, (350, 100))

#High Score
high_score_button_image = pygame.image.load("images/buttons/high_score_btn.png")
high_score_button_image = pygame.transform.scale(high_score_button_image, (350, 100))

#Name font
name_font = pygame.font.Font("freesansbold.ttf", 64)

#Score font
score_font = pygame.font.Font("freesansbold.ttf", 32)

def name_text(screen):
    name_text = name_font.render("Input your name", True, (255,255,255))
    screen.blit(name_text, (275, 150))

class OverScreen:

    def __init__(self, screen):
        self.screen = screen

    # Verify if continue button was clicked
    def check_continue_click(mouse_pos):
        continue_button_rect = continue_button_image.get_rect(topleft=(500, 300))
        if continue_button_rect.collidepoint(mouse_pos):
            return True
        return False

    # Verify if high score button was clicked
    def check_high_score_click(mouse_pos):
        high_score_button_rect = high_score_button_image.get_rect(topleft=(500, 450))
        if high_score_button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def get_user_name(self, score):
        # Define the initial position for the input box
        input_box_width = 140
        input_box_x = (1080 - input_box_width) // 2
        input_box = pygame.Rect(input_box_x, 300, input_box_width, 32)

        # Create the Enter button
        enter_button = pygame.Rect(440, 350, 200, 32)  # Adjusted position and size of the button
        # Create the colors of the input box when it is active and inactive
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')

        # Set default color as inactive
        color = color_inactive

        # Set active attribute for the textbox to false
        active = False

        # Set the default text to empty
        text = ''

        # When this variable is true, the while loop will end
        done = False

        # Maximum number of allowed letters
        max_letters = 3

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # If the mouse button collides with the input box, activate it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    elif enter_button.collidepoint(event.pos) and len(text) > 0:
                        done = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN and len(text) > 0:
                            done = True
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text) < max_letters:
                                text += event.unicode

            self.screen.fill((30, 30, 30))

            # Adjust the position of the input box to center it on the screen
            input_box.x = (1080 - input_box_width) // 2

            name_text(self.screen)

            # Show user score
            score_text = score_font.render("Your score: " + str(score), True, (255, 255, 255))
            score_text_rect = score_text.get_rect(center=(1080 // 2, 250))
            self.screen.blit(score_text, score_text_rect.topleft)

            font = pygame.font.Font(None, 32)

            txt_surface = font.render(text, True, color)

            # Adjusted the position to center the text in the input box
            self.screen.blit(txt_surface, ((1080 - txt_surface.get_width()) // 2, input_box.y + 5))

            # Draw the input box
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Draw Enter button
            pygame.draw.rect(self.screen, color_inactive, enter_button, 2)

            font_enter = pygame.font.Font(None, 32)
            text_enter = font_enter.render("Enter", True, (255, 255, 255))

            # Adjust the position to center the text in the button
            text_enter_rect = text_enter.get_rect(center=enter_button.center)
            self.screen.blit(text_enter, text_enter_rect.topleft)

            pygame.display.update()

        return text

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        self.screen.blit(continue_button_image, (500, 300))
        self.screen.blit(high_score_button_image, (500, 450))