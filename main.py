import collision_functions
import delivery_man
import spritesheet
import pygame
import random
import json
import numpy as np
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

#Background Sound
mixer.music.load("music/background_music.mp3")
mixer.music.play(-1)

#Order font
order_font = pygame.font.Font("fuentes/dogica.ttf", 30)
delivered_font = pygame.font.Font("fuentes/dogica.ttf", 20)
over_font = pygame.font.Font("fuentes/Daydream.ttf", 64)
score_font  = pygame.font.Font("fuentes/Daydream.ttf", 35)
time_left_font = pygame.font.Font("fuentes/dogica.ttf", 30)

#Crear variables de imágenes
meat_img = pygame.image.load("images/buttons/boton_carne.jpg").convert_alpha()
lech_img = pygame.image.load("images/buttons/boton_lechuga.jpg").convert_alpha()
toma_img = pygame.image.load("images/buttons/boton_tomate.jpg").convert_alpha()
fish_img = pygame.image.load("images/buttons/button_L.png").convert_alpha()
cheese_img = pygame.image.load("images/buttons/button_J.png").convert_alpha()
onion_img = pygame.image.load("images/buttons/button_F.png").convert_alpha()

##----------------------------------------------------------------------------------------------

##daclare acceleration (GRAVITY)
GRAVITY = 2
ACCX = 3

## How much the object will bounce in a collision, must be a balue between 0 and 1
REBOTE = 0.5

#Define Coord where the first element will make collision
FLOOR_VALUE =  449

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

objects_height = {'Lettuce':10,'Tomatoe':5,'Meat':20,'Top_bun':60,'Under-bun':20, "Cheese":5, "Fish":20, "Onion":5}
objects_x = {'Lettuce':449,'Tomatoe':480,'Meat':460,'Top_bun':444,'Under-bun':444,"Cheese":455, "Fish":420, "Onion":460}

available_ingredients = ("Lettuce", "Tomatoe", "Meat", "Cheese", "Fish", "Onion", "Top_bun", "Under-bun")

pressed_keys = []

# Setting up the coordinates that will be substracted from the coordinates of every object, giving the illusion of a camera
camera_x = 0
camera_y = 0

camera_central_point_x = 0
camera_central_point_y = 0
camera_central_point_x_extra = 0
camera_central_point_y_extra = 0
# The bigger the nunmber, the more tank-ish the camera feels
CAMERA_SPEED = 10

SPEECH_SPRITES_LENGHT = 644
SPEECH_SPRITES_HEIGHT = 420


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
        screen.blit(self.image, (self.xPosition - camera_x, self.yPosition - camera_y))

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
        self.screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class just_an_image():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self, parallax):
        screen.blit(self.image, (self.x - camera_x * parallax, self.y - camera_y * parallax))

class speech_bubble():
    def __init__(self, ss, x, y):
        self.ss = ss
        self.x = x
        self.y = y
        self.sheet_x = 0
        self.sheet_y = 0
        self.animation_frame = 0

    def draw(self, parallax):
        speech_costume = self.ss.imgat((self.sheet_x * SPEECH_SPRITES_LENGHT, self.sheet_y * SPEECH_SPRITES_HEIGHT, SPEECH_SPRITES_LENGHT, SPEECH_SPRITES_HEIGHT))
        screen.blit(speech_costume, (self.x - camera_x * parallax, self.y - camera_y * parallax))

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
    item = food_element(objects_x[name], camera_y - 90, name, objects_height[name])
    object_order.append(item)
    if name != 'Top_bun'and name != 'Under-bun':
        number_elements_list[available_ingredients.index(name)] += 1

def show_score(x, y):
    score_text = score_font.render("Score : " + str(score_value), True, (255,255,228))
    screen.blit(score_text, (x, y))

def show_order(requested_order):
    order_message = ""
    for i in range(len(requested_order)):

        order_message += str(requested_order[i][0]) + " x " + str(requested_order[i][1]) + "\n"
    
    return order_message

def draw_order_text(x, y, space, parallax):
    ##Drawing the order text
    for line in lines:
        print(show_message)
        text_surface = order_font.render(line, True, (52,17,31))

        if not hide_text_order:
            screen.blit(text_surface, (x - np.cos(pygame.time.get_ticks()/100)*10 - camera_x * parallax, y - camera_y * parallax))  # Adjust the position of the text
                
        y += space  # Ajust the spaces between lines

def calculate_min_max_order(completed_orders):
    min_ord = completed_orders//3 + 1

    max_ord = completed_orders//3 + 3

    if min_ord > 3:
        min_ord = 3

    if max_ord > 5:
        max_ord = 5

    return min_ord, max_ord

#create customer order
def create_order(completed_orders):
    min_ord, max_ord = calculate_min_max_order(completed_orders)

    lettuce_num = random.randint(min_ord,max_ord)
    tomato_num = random.randint(min_ord,max_ord)
    meat_num = random.randint(min_ord,max_ord)

    if completed_orders < 3:
        cheese_num = 0
        fish_num = 0
        onion_num = 0
    elif completed_orders < 8:
        cheese_num = random.randint(min_ord,max_ord)
    elif completed_orders < 15:
        fish_num = random.randint(min_ord,max_ord)
    else:
        onion_num = random.randint(min_ord,max_ord)


    #Position 0 --> n elements
    #position 1 --> name element
    lettuce_tuple = (lettuce_num, "lettuce")
    tomato_tuple = (tomato_num, "tomato")
    meat_tuple = (meat_num, "meat")
    cheese_tuple = (cheese_num, "cheese")
    onion_tuple = (onion_num, "onion")
    fish_tuple = (fish_num, "fish")

    #This will be the requested order array that will be compared with the user delivered order
    requested_order = [lettuce_num, tomato_num, meat_num, cheese_num, fish_num, onion_num]

    #This will save the order distribution in the screen (will be different every time)
    order_distribution = [lettuce_tuple, tomato_tuple, meat_tuple, cheese_tuple, fish_tuple, onion_tuple]

    #Shuffle the requested order list to show the elements in different order
    random.shuffle(order_distribution)

    return (requested_order, order_distribution)

def game_over_text():
    over_text = over_font.render("GAME OVER : ", True, (255,255,228))
    screen.blit(over_text, (200, 250))

def score_to_get(order_quantity_list):
    score_to_get = 0
    for quantity in order_quantity_list:
        score_to_get += quantity
    return score_to_get

def deliver_order():
    global gamestate, message_display_time, score_value, completed_orders, show_order_status, order_distribution, start_time, requested_order, number_elements_list, angry_bar
    gamestate = 2
    message_display_time -= 100
    create_food_instance("Top_bun")

    # for i in range(len)
    print("Requested order:", requested_order)
    print("Number elements list: ", number_elements_list)

    if start_time == 0:
        start_time = pygame.time.get_ticks()
                    
    if requested_order == number_elements_list:
        message = True
        score_value += score_to_get(requested_order)  
        completed_orders += 1
    else:
        message = False
        if angry_bar.angriness < 100:
            angry_bar.angriness += 25

    message = delivered_font.render(f"Order delivered {('incorrectly','successfully')[message]}", True, ((255, 255, 228),(156, 185, 59))[message])

    show_order_status = True
    requested_order = None
    order_distribution = None
    number_elements_list = [0,0,0,0,0,0]

    return message

def restart_game():
    global time_limit, completed_orders, object_order, number_elements_list, start_time, elapsed_time, message_display_time, show_message
    global requested_order, order_distribution, score_value, angry_bar, show_order_status, order_status_time, gamestate, hide_text_order, guy, head

    completed_orders = 0
    
    object_order = []

    #This array will get the number of each element
    number_elements_list = [0,0,0,0,0,0]

    # Time tracking variables
    start_time = 0
    elapsed_time = 0
    show_order_status = False
    order_status_time = 2000
    message_display_time = 5000
    show_message = True

    ##States if the player may have input or not
    gamestate = 4

    #Initialize requested order & distribution variables
    requested_order = None
    order_distribution = None

    ##Draw order text
    hide_text_order = 0

    #Score
    score_value = 0
    angry_bar = AngryBar(10, 10, 300, 40, 100)

    time_limit = 40

    #Declare Delivery guy
    guy = delivery_man.the_guy(screen, -200, 260)
    head = delivery_man.the_guy_head(guy)

#set instances-------------------------------------------------------------------------------------------------------------------
restart_game()

table_image = pygame.image.load('images/other_objects/mesa_verde_2.png').convert_alpha()
table = just_an_image(table_image, -100, 376)

expanded_background_image = pygame.image.load('images/Fondos/expanded_background_4.png').convert_alpha()
expanded_background = just_an_image(expanded_background_image, -100, -280)

speech_sprite_sheet = spritesheet.get_spritesheet('images/other_objects/speech_bubble.png')
speech = speech_bubble(speech_sprite_sheet, -20, -150)

#Buttons dimensions
meat_button = button(20, 600, meat_img, 0.2, screen)
lechu_button = button(200, 600, lech_img, 0.2, screen)
toma_button = button(380, 600, toma_img, 0.2, screen)
fish_button = button(555, 600, fish_img, 0.2, screen)
cheese_button = button(720, 600, cheese_img, 0.2, screen)
onion_button = button(885, 600, onion_img, 0.2, screen)

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

                if cheese_button.check_clicked_button(mouse_pos):
                    create_food_instance("Cheese")

                if fish_button.check_clicked_button(mouse_pos):
                    create_food_instance("Fish")

                if onion_button.check_clicked_button(mouse_pos):
                    create_food_instance("Onion")

    # Refresh and draw the menu screen
    if draw_menu:
        menu.draw()

    elif start_game:

        #Just a cute feature to give the player semi-controll of the camera
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            camera_central_point_y_extra = 40
        elif pressed[pygame.K_DOWN]:
            camera_central_point_y_extra = -40
        else: camera_central_point_y_extra = 0

        if pressed[pygame.K_LEFT]:
            camera_central_point_x_extra = 40
        elif pressed[pygame.K_RIGHT]:
            camera_central_point_x_extra = -40
        else: camera_central_point_x_extra = 0

        camera_y += round((camera_central_point_y + camera_central_point_y_extra - camera_y) / CAMERA_SPEED)
        camera_x += round((camera_central_point_x + camera_central_point_x_extra - camera_x) / CAMERA_SPEED)

        #Defining keys that will ba counted as input
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

            if lock_key(pygame.K_j):
                create_food_instance("Cheese")

            if lock_key(pygame.K_l):
                create_food_instance("Fish")

            if lock_key(pygame.K_f):
                create_food_instance("Onion")

            if lock_key(pygame.K_SPACE):
                start_time = 0
                message = deliver_order()
                #NOTE, TUVE QUE USAR LAS SIGUIENTES VARIABLES EN GLOBAL EN LA FUNCION

                # gamestate = 2
                # message_display_time -= 100
                # create_food_instance("Top_bun")

                # print("Requested order:", requested_order)
                # print("Number elements list: ", number_elements_list)

                # if start_time == 0:
                #     start_time = pygame.time.get_ticks()
                                
                # if requested_order == number_elements_list:
                #     message = True
                #     score_value += score_to_get(requested_order)  
                #     completed_orders += 1
                # else:
                #     message = False
                #     if angry_bar.angriness < 100:
                #         angry_bar.angriness += 25

                # message = delivered_font.render(f"Order delivered {('incorrectly','successfully')[message]}", True, ((255,0,0),(0,255,0))[message])
                # show_order_status = True
                # requested_order = None
                # order_distribution = None
                # number_elements_list = [0,0,0]

        if start_time == 0:
            start_time = pygame.time.get_ticks()

        fps.tick(30)
        
        #Orden en el que dibujar cada objeto en pantalla
        expanded_background.draw(parallax = 0.25)
        #Se comparte la posición de la cámara con otro módulo
        delivery_man.get_camera(guy, camera_x, camera_y)
        #Se ejecutan todos los procesos relacionados al repartidor.
        delivery_man.delivery(gamestate, guy, head, pygame.time.get_ticks())

        if delivery_man.send_changes_in_gamestate():
            gamestate = delivery_man.send_changes_in_gamestate()

        table.draw(parallax = 1)

        #Draw buttons
        meat_button.draw()
        lechu_button.draw()
        toma_button.draw()
        fish_button.draw()
        cheese_button.draw()
        onion_button.draw()

        if requested_order == None:
            requested_order, order_distribution = create_order(completed_orders)

        # Show the requested order message
        order_text = show_order(order_distribution)
        lines = order_text.split('\n')

        #Draw angry bar
        angry_bar.draw(screen)

        #Game over
        if angry_bar.angriness == 100:
            start_game = False
            input_name = True

        # Calculate the time elapsed in seconds
        # Time limit code
        if gamestate == 1:
            elapsed_time_seconds = (pygame.time.get_ticks() - start_time) // 1000
            time_left = time_limit - elapsed_time_seconds

            if time_left <= 10: time_text_color = (217, 36, 60)
            else: time_text_color = (119, 214, 193)

            time_left_message = time_left_font.render("Time left:" + str(time_left), True, time_text_color)
            time_left_message_white = time_left_font.render("Time left:" + str(time_left), True, (255, 255, 228))
            screen.blit(time_left_message, (10,78))
            screen.blit(time_left_message_white, (10,75))

            #Deliver order
            if time_left <= 0:
                start_time = 0
                message = deliver_order()

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
            if elapsed_time >= message_display_time / 2:
                show_order_status = False

        ##Print score on screen
        show_score(scoreX, scoreY)

        ##Everything having to do with changes in gamestate

        ##Animation for hamburger dash when an order is delivered
        for i in range(len(object_order)):

            if gamestate == 3:
                object_order[i].spdx += ACCX

            object_order[i].spdy += GRAVITY
            object_order[i].xPosition += object_order[i].spdx

            if object_order[i].move == True or i == 0:
                object_order[i].yPosition += object_order[i].spdy
                collision_functions.check_collisions(object_order[i], object_order[i-1], REBOTE, FLOOR_VALUE)

            object_order[i].draw()

        ##changes in camera
        if gamestate == 4:
            speech.animation_frame = 0

            ## We delete all food items
            object_order = []

        elif gamestate == 5:
            camera_central_point_y = -200

            ##Draw speech_bubble
            speech.sheet_x = np.floor(speech.animation_frame % 7)
            speech.draw(parallax = 0.6)

            if speech.animation_frame < 6:
                speech.animation_frame += 0.5
            else:
                ##Drawing the order text
                draw_order_text(110, -50, space = 40, parallax = 0.5)

        elif gamestate == 6:
            camera_central_point_y = 0
            speech.draw(parallax = 0.6)

        else:
            if speech.animation_frame > 0:
                speech.animation_frame -= 0.5
                speech.sheet_x = np.floor(speech.animation_frame % 7)
                speech.draw(parallax = 0.6)

        ##Check if there exists food elements on screen
        if len(object_order):

            if object_order[-1].move == False and gamestate == 2:
                gamestate = 3
                show_message = True
                hide_text_order = 0

            if  object_order[0].xPosition > 1200 and gamestate == 3:
                gamestate = 7
        else: 
            if gamestate == 3:
                create_food_instance("Under-bun")
                object_order[0].move = False
                gamestate = 1
        

    #End of main game loop
                
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