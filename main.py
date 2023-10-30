import collision_functions
import pygame
import random
import json
import numpy
from pygame import mixer

#Import objects from other files
from menu_screen import MenuScreen
from game_over_screen import OverScreen
from highscore_screen import HighScoreScreen

##pygame related variables-------------------------------------------------------------------------

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption("Hamburguer Fever")

#Background
background_image = pygame.image.load("images/Fondos/Fondo1.png")
background_image = pygame.transform.scale(background_image, (1080, 720))

#Background Sound
mixer.music.load("music/background_music.mp3")
mixer.music.play(-1)

#Order font
order_font = pygame.font.Font("fuentes/dogica.ttf", 20)
delivered_font = pygame.font.Font("fuentes/dogica.ttf", 20)
over_font = pygame.font.Font("fuentes/Daydream.ttf", 64)
score_font  = pygame.font.Font("fuentes/Daydream.ttf", 35)

#Crear variables de imágenes
meat_img = pygame.image.load("images/buttons/boton_carne.jpg").convert_alpha()
lech_img = pygame.image.load("images/buttons/boton_lechuga.jpg").convert_alpha()
toma_img = pygame.image.load("images/buttons/boton_tomate.jpg").convert_alpha()

##----------------------------------------------------------------------------------------------

##daclare acceleration (GRAVITY)
GRAVITY = 2
ACCX = 3

## How much the object will bounce in a collision, must be a balue between 0 and 1
REBOTE = 0.5

#Define Coord where the first element will make collision
FLOOR_VALUE =  450

#Menu screen object
menu = MenuScreen(screen)

#Over screen object
game_over = OverScreen(screen)

#High Score screen object
high_score = HighScoreScreen(screen)

#Determine if the menu has to be drawn or no
draw_menu = True

#Determine if the game is started
start_game = False

#Request the user to input name
input_name = False

#Determine if the game has finished
draw_game_over = False

#Draw high scores
draw_high_scores = False

scoreX = 420
scoreY = 52

objects_height = {'Lettuce':10,'Tomatoe':4,'Meat':20,'Top_bun':60,'Under-bun':20}
objects_x = {'Lettuce':456,'Tomatoe':480,'Meat':460,'Top_bun':444,'Under-bun':444}

available_ingredients = ('Lettuce','Tomatoe','Meat','Top_bun','Under-bun')

pressed_keys = []

##classes-------------------------------------------------------------------------------------

class food_element():
    def __init__(self, x, y, food_name, height):
        self.xPosition = x
        self.yPosition = y
        self.food_name = food_name
        self.image = None
        self.spdy = 0
        self.spdx = 0
        self.move = True
        self.calculo_REBOTE = 0
        self.height = height
    
    def draw(self):
        self.image = pygame.image.load("images/food/Final_Sprites/" + self.food_name + ".png").convert_alpha()
        screen.blit(self.image, (self.xPosition, self.yPosition))

class AngryBar():
    def __init__(self, x, y, w, h, max_angriness):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.angriness = 0
        self.max_angriness = max_angriness

    def draw(self, surface):
        #Calculate angriness ratio
        ratio = self.angriness / self.max_angriness
        pygame.draw.rect(surface, "gray", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))

class button():
    def __init__(self,x,y,image,scale,screen): #Cuando se usa pygame todo es con imágenes, primero la imágen y luego se importa, incluso el texto.
        width=image.get_width()
        height=image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))#Para pixeles solo se trabaja con float
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y) #A partir de estas coordenadas se crea el botón
        self.screen = screen

    def check_clicked_button(self, mouse_pos):
        #Ver posición del mouse
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self):
        #impresión imágen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

##functions-------------------------------------------------------------------------------------

def lock_key(key):
    pressed = pygame.key.get_pressed()
    if pressed[key]:
        if not key in pressed_keys:
            pressed_keys.append(key)
            return True
    else:
        if key in pressed_keys:
            pressed_keys.pop(pressed_keys.index(key))

def create_food_instance(name):
    item = food_element(objects_x[name], -70, name, objects_height[name])
    object_order.append(item)
    if name != 'Top_bun'and name != 'Under-bun':
        number_elements_list[available_ingredients.index(name)] += 1

def show_score(x, y):
    score_text = score_font.render("Score : " + str(score_value), True, (255,255,228))
    screen.blit(score_text, (x, y))

def show_order(requested_order):
    order_message = ""
    for i in range(len(requested_order)):

        element_name = ("Lettuce","Tomatoe","Meat")[i]
        order_message += str(requested_order[i]) + " x " + str(element_name) + "\n"
    
    return order_message

#create customer order
def create_order():
    lettuce_num = random.randint(0,3)
    tomato_num = random.randint(0,3)
    meat_num = random.randint(1,3)
    requested_order = [lettuce_num, tomato_num, meat_num]

    return requested_order

def game_over_text():
    over_text = over_font.render("GAME OVER : ", True, (255,255,228))
    screen.blit(over_text, (200, 250))

def score_to_get(order_quantity_list):
    score_to_get = 0
    for quantity in order_quantity_list:
        score_to_get += quantity
    return score_to_get

def restart_game():
    global object_order, number_elements_list, start_time, elapsed_time, message_display_time, show_message, requested_order, score_value, angry_bar, show_order_status, deliver_order, order_status_time, gamestate, hide_text_order
    #deliver order
    deliver_order = False
    object_order = []

    #This array will get the number of each element
    number_elements_list = [0,0,0]

    # Time tracking variables
    start_time = 0
    elapsed_time = 0
    show_order_status = False
    order_status_time = 2000
    message_display_time = 5000
    show_message = True

    ##States if the player may have input or not
    gamestate = 0

    #Initialize requested order variable
    requested_order = None

    ##Draw order text
    hide_text_order = 0

    #Score
    score_value = 0
    angry_bar = AngryBar(10, 10, 300, 40, 100)

#set instances-------------------------------------------------------------------------------------------------------------------
restart_game()

meat_button = button(200, 600, meat_img, 0.2, screen)
lechu_button = button(400, 600, lech_img, 0.2, screen)
toma_button = button(600, 600, toma_img, 0.2, screen)

fps = pygame.time.Clock()
elapsed_time = 0
running = True

#game loop------------------------------------------------------------------------------------------------------------------------
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if draw_menu:
                if MenuScreen.check_exit_click(mouse_pos):
                    running = False
                if MenuScreen.check_start_click(mouse_pos):
                    draw_menu = False
                    start_game = True
            if draw_game_over:
                if OverScreen.check_continue_click(mouse_pos):
                    draw_menu = True
                    draw_game_over = False
                    restart_game()
                if OverScreen.check_high_score_click(mouse_pos):
                    draw_game_over = False
                    draw_high_scores = True
            if draw_high_scores:
                    if HighScoreScreen.check_return_click(mouse_pos):
                        draw_menu = True
                        draw_high_scores = False
                        restart_game()
        if start_game:
            if event.type == pygame.MOUSEBUTTONDOWN and gamestate == 1:
                mouse_pos = pygame.mouse.get_pos()
                #Botones de visualización y funcionalidad
                if meat_button.check_clicked_button(mouse_pos):
                    create_food_instance("Meat")

                if lechu_button.check_clicked_button(mouse_pos):
                    create_food_instance("Lettuce")

                if toma_button.check_clicked_button(mouse_pos):
                    create_food_instance("Tomatoe")

    # Refresh and draw the menu screen
    if draw_menu:
        menu.draw()

    elif start_game:

        if gamestate == 1:
            if lock_key(pygame.K_r):
                draw_menu = False
                start_game = False
                draw_game_over = True
                input_name = False

            if lock_key(pygame.K_t):
                draw_menu = False
                start_game = False
                draw_game_over = False
                input_name = True

            if lock_key(pygame.K_s):
                create_food_instance("Lettuce")

            if lock_key(pygame.K_k):
                create_food_instance("Tomatoe")

            if lock_key(pygame.K_d):
                create_food_instance("Meat")

            if lock_key(pygame.K_SPACE):
                gamestate = 2
                message_display_time -= 100
                create_food_instance("Top_bun")

                if start_time == 0:
                    start_time = pygame.time.get_ticks()
                                
                if requested_order == number_elements_list:
                    message = True
                    score_value += score_to_get(requested_order)  
                else:
                    message = False
                    if angry_bar.angriness < 100:
                        angry_bar.angriness += 25

                message = delivered_font.render(f"Order delivered {('incorrectly','successfully')[message]}", True, ((255,0,0),(0,255,0))[message])
                show_order_status = True
                requested_order = None
                number_elements_list = [0,0,0]

        fps.tick(30)
        print(hide_text_order)
        screen.fill((0,0,0))
        screen.blit(background_image, (0,0))

        #Draw buttons
        meat_button.draw()
        lechu_button.draw()
        toma_button.draw()

        show_score(scoreX, scoreY)

        if requested_order == None:
            requested_order = create_order()

        # Show the requested order message
        order_text = show_order(requested_order)
        lines = order_text.split('\n')
        y = 20  # Initial y position

        for line in lines:
            text_surface = order_font.render(line, True, (255,255,228))

            if show_message and not hide_text_order:
                screen.blit(text_surface, (810 - numpy.cos(pygame.time.get_ticks()/100)*10, y))  # Adjust the position of the text
                
            y += 30  # Ajust the spaces between lines

        #Draw angry bar
        angry_bar.draw(screen)

        #Game over
        if angry_bar.angriness == 100:
            start_game = False
            input_name = True

        # Show the message for 2 seconds
        # Show the message for a specified duration
        if show_message and score_value > 0:
            #Subtract to the current time the time when the spacebar was pressed
            elapsed_time = pygame.time.get_ticks() - start_time
            #Check if the time is higher than the message display time specified
            if elapsed_time >= message_display_time:
                show_message = False
                start_time = 0  # Reset the start time
                elapsed_time = 0  # Reset the elapsed time
            elif elapsed_time >= message_display_time - message_display_time/5:
                hide_text_order = abs(hide_text_order - 1)

        if show_order_status:
            elapsed_time = pygame.time.get_ticks() - start_time
            screen.blit(message, (10, 120))
            if elapsed_time >= message_display_time/2:
                show_order_status = False


        for i in range(len(object_order)):

            if gamestate == 3:
                object_order[i].spdx += ACCX

            object_order[i].spdy += GRAVITY
            object_order[i].xPosition += object_order[i].spdx

            if object_order[i].move == True or i == 0:
                object_order[i].yPosition += object_order[i].spdy
                collision_functions.check_collisions(object_order[i], object_order[i-1], REBOTE, FLOOR_VALUE)

            object_order[i].draw()

        if len(object_order):

            if object_order[-1].move == False and gamestate == 2:
                gamestate = 3
                show_message = True
                hide_text_order = 0

            if  object_order[0].xPosition > 1200 and gamestate == 3:
                object_order = []
        else: 
            create_food_instance("Under-bun")
            object_order[0].move = False
            gamestate = 1
            
    elif input_name:
            user_name = game_over.get_user_name(score_value)
            if user_name:
                input_name = False
                draw_game_over = True

                try:
                    #with guarantees that the resources are released at the end of the code block
                    #So here we are opening a file and creating a hanlde named archivo. At the end of the execution of the 
                    #with, it will close
                    with open("Hamburger_Fever_Scores.txt", "r") as archivo:
                        #Here we store the lines of the file in an array
                        data = archivo.readlines()

                        #We create the dictionary of scores
                        scores_dict = {}
                        
                        #We are going to iterate for each line in data
                        for line in data:
                            #Here, we get the original JSON chain (which is a dictionary and save it in store_data -> It will be a dictionary)
                            score_data = json.loads(line)
                            #Update the dictionary with the key-value pair from score_data dictionary
                            scores_dict.update(score_data)

                #If there is no file, we create a new dictionary
                except FileNotFoundError:
                    scores_dict = {}

                # Verify if the username is alredy in the dictionary and update if it is necesary
                if user_name in scores_dict:
                    #If the current score is greater than the dictionary score, we update it
                    if score_value > scores_dict[user_name]:
                        scores_dict[user_name] = score_value
                #If there is no registered  name, we store the score in a new key
                else:
                    scores_dict[user_name] = score_value

                #Convert the scores dictionary to a string in JSON format. (To store data in json format and then be able to recover it when a user name is entered)
                text_to_file = json.dumps(scores_dict)

                #Write the names and scores into the 'Hamburger_Fever_Scores.txt' file
                with open("Hamburger_Fever_Scores.txt", "w") as archivo:
                    archivo.write(text_to_file + "\n")

    elif draw_game_over:
        game_over.draw()

    elif draw_high_scores:
        high_score.draw()
        
    # Refresh the screen
    pygame.display.update()