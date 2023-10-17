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
        # Create the Enter button
        enter_button = pygame.Rect(540, 350, 140, 32)
        #Create the colors of the input box when it is active and unactive
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')

        #Set default color as inactive
        color = color_inactive

        #Set active attribute for the textbox in false
        active = False

        #Set the default text empty
        text = ''

        #Wehn this variable is true, the while loop will end
        done = False

        # Maximum number of allowed letters
        max_letters = 3  

        while not done:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                #If the mouse button collides with the input box, active it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                        # Check if 'Enter' button is clicked and text is not empty
                    elif enter_button.collidepoint(event.pos) and len(text) > 0:
                        done = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        #If the input box is active, when backspace is clicked, delete one letter from the text string
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            # Check the maximum letters and add a letter if the string is no longer than 3
                            if len(text) < max_letters:
                                text += event.unicode
            
            #Fill the screen with a color
            self.screen.fill((30, 30, 30))

            #Show the text that request the user to input it's name
            name_text(self.screen)

            #Set the font and size it to 32

            font = pygame.font.Font(None, 32)

            #Show the text in the input box
            txt_surface = font.render(text, True, color)
            input_box.w = 200
            self.screen.blit(txt_surface, ((1080 - txt_surface.get_width()) // 2, input_box.y + 5))

            #Rect(screen, color, position and size, border thickness)
            #Draw the input box
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Draw Enter button
            pygame.draw.rect(self.screen, color_inactive, enter_button, 2)  
            font_enter = pygame.font.Font(None, 32)
            text_enter = font_enter.render("Enter", True, (255, 255, 255))
            self.screen.blit(text_enter, (enter_button.x + 10, enter_button.y + 5))  # Position the 'Enter' button text

            pygame.display.flip()

        return text

    def draw(self):
        self.screen.blit(background_menu_image, (0,0))
        self.screen.blit(continue_button_image, (150,600))
        self.screen.blit(high_score_button_image, (550,600))
