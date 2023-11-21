import pygame
import json

pygame.init()

#Background
background_over_image = pygame.image.load("images/high_score_background.png")
background_menu_image = pygame.transform.scale(background_over_image, (1080, 720))

#Continue
main_menu_button_image = pygame.image.load("images/buttons/main_menu_btn.png")
main_menu_button_image = pygame.transform.scale(main_menu_button_image, (400, 65))

#Title font
title_font = pygame.font.Font("freesansbold.ttf", 64)

# Font configuration
font = pygame.font.Font("freesansbold.ttf", 36)

def title_text(screen):
    title_text = title_font.render("Leaderboard", True, (255,255,255))
    screen.blit(title_text, (250, 150))

class HighScoreScreen:

    def __init__(self, screen):
        self.screen = screen
        
    # Verify if the return button was clicked
    def check_return_click(mouse_pos):
        main_menu_x = (1080 - main_menu_button_image.get_width()) // 2
        main_menu_button_image_button_rect = main_menu_button_image.get_rect(topleft=(main_menu_x, 635))
        if main_menu_button_image_button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def load_sort_scores(self):
        with open("Hamburger_Fever_Scores.txt", "r") as file:
            high_scores = []
            for line in file:
                score_data = json.loads(line)
                for key, value in score_data.items():
                    high_scores.append((key, value))

        # Bubble sort
        n = len(high_scores)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if high_scores[j][1] < high_scores[j + 1][1]:
                    high_scores[j], high_scores[j + 1] = high_scores[j + 1], high_scores[j]

        return high_scores
                    
    def draw_scores(self):
        high_scores = self.load_sort_scores()
        #Vertical scroll for each score line
        y_offset = 280
        #Obtain the top high scores
        top_scores = high_scores[:5]

        for i, (name, score) in enumerate(top_scores):
            score_text = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 255))
            score_x = (1080 - score_text.get_width()) // 2
            score_y = y_offset + i * 50
            self.screen.blit(score_text, (score_x, score_y))        

    def draw(self):
        self.screen.blit(background_menu_image, (0, 0))
        main_menu_x = (1080 - main_menu_button_image.get_width()) // 2
        self.screen.blit(main_menu_button_image, (main_menu_x, 635))

        self.draw_scores()
