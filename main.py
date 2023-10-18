import pygame
import random
import botones
import json

#Handle music in the game
from pygame import mixer

#Import the menu screen
from menu_screen import MenuScreen
from game_over_screen import OverScreen
from highscore_screen import HighScoreScreen

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption("Hamburguer Fever")

#Menu screen object
menu = MenuScreen(screen)

#Over screen object
game_over = OverScreen(screen)

#High Score screen object
high_score = HighScoreScreen(screen)

#Background
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (1080, 720))

#Background Sound
mixer.music.load("music/background_music.mp3")
mixer.music.play(-1)

#Order font
order_font = pygame.font.Font("freesansbold.ttf", 20)

#Delivered order font
delivered_font = pygame.font.Font("freesansbold.ttf", 20)

#Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

#deliver order
deliver_order = False

object_order = []

#This array will get the number of each element
#   bottom_bread -> 0
#   meat -> 1
#   lettuce -> 2
#   tomato -> 3
#   top_bread -> 4
number_elements_list = [0,0,0]

# Time tracking variables
start_time = 0
elapsed_time = 0
message_display_time = 2000
show_message = False

##daclare acceleration (gravity)
gravity = 2
accx = 3

## How much the object will bounce in a collision, must be a balue between 0 and 1
rebote = 0.5

##States if the player may have input or not
gamestate = 0

#Initialize requested order variable
requested_order = None

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

#Score
score_value = 0
score_font  = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 500
scoreY = 10

#Crear variables de imágenes
meat_img = pygame.image.load("images/buttons/boton_carne.jpg").convert_alpha()
lech_img = pygame.image.load("images/buttons/boton_lechuga.jpg").convert_alpha()
toma_img = pygame.image.load("images/buttons/boton_tomate.jpg").convert_alpha()

#Tamaño imágenes - botones comida
meat_button = botones.button(200, 600, meat_img, 0.2, screen)
lechu_button = botones.button(400, 600, lech_img, 0.2, screen)
toma_button = botones.button(600, 600, toma_img, 0.2, screen)

class food_element():
    def __init__(self, x, y, food_name):
        self.xPosition = x
        self.yPosition = y
        self.food_name = food_name
        self.image = None
        self.spdy = 0
        self.spdx = 0
        self.move = True
        self.calculo_rebote = 0
        self.height = 20
    
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

#Create an angry bar object
angry_bar = AngryBar(10, 10, 300, 40, 100)

def show_score(x, y):
    score_text = score_font.render("Score : " + str(score_value), True, (102,0,204))
    screen.blit(score_text, (x, y))

def isCollision(object2_y,object1_y,i):
    # Distance between two points D = sqrt*(x2 - x1)^2 + (y2 - y1)^2)
    if i == 0:
        if object_order[i].yPosition > 550:
            return True
    elif object1_y - object_order[i-1].height / 2 < object2_y + object_order[i].height:
        return True
    else: return False

def show_order_delivered_message(successful):
    if successful:
        delivered_message = delivered_font.render("Order delivered successfully", True, (0,255,0))
    else:
        delivered_message = delivered_font.render("Order delivered incorrectly", True, (255,0,0))
    return delivered_message

def show_order(requested_order):
    order_message = ""
    for i in range(len(requested_order)):
        if i == 0:
            element_name = "Lettuce"
        elif i == 1:
            element_name = "Tomatoe"
        elif i == 2:
            element_name = "Meat"

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
    over_text = over_font.render("GAME OVER : ", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def check_collisions(i):

    if isCollision(object_order[i].yPosition, object_order[i - 1].yPosition,i):
        object_order[i].calculo_rebote = -(abs(object_order[i].spdy) * rebote)
        
        if object_order[i].calculo_rebote < -1.5:
            object_order[i].spdy = object_order[i].calculo_rebote
            object_order[i].yPosition += object_order[i].spdy
        else:
            object_order[i].spdy = 0

            if object_order[i-1].move == False:
                object_order[i].move = False

    while isCollision(object_order[i].yPosition, object_order[i - 1].yPosition,i):
        object_order[i].yPosition -= 1

def score_to_get(order_quantity_list):
    score_to_get = 0
    for quantity in order_quantity_list:
        score_to_get += quantity
    return score_to_get

def restart_game():
    # Restarting the global variables
    global object_order, number_elements_list, start_time, elapsed_time, message_display_time, show_message, gravity, requested_order, score_value, angry_bar
    object_order = []
    number_elements_list = [0,0,0]
    start_time = 0
    elapsed_time = 0
    message_display_time = 2000
    show_message = False
    gravity = 2
    requested_order = None
    score_value = 0
    angry_bar = AngryBar(10, 10, 300, 40, 100)

def slide():
    return

fps = pygame.time.Clock()

running = True
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
                    print("Starting game...")
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
                    print("Pressed: button meat")
                    meat = food_element(460, -70, "Meat")
                    object_order.append(meat)
                    number_elements_list[2] += 1

                if lechu_button.check_clicked_button(mouse_pos):
                    print("Pressed: button lettuce")
                    lettuce = food_element(456, -70, "Lettuce")
                    object_order.append(lettuce)
                    object_order[-1].height = 10
                    number_elements_list[0] += 1

                if toma_button.check_clicked_button(mouse_pos):
                    print("Pressed: button tomatoe")
                    tomato = food_element(480, -70, "Tomatoe")
                    object_order.append(tomato)
                    object_order[-1].height = 3
                    number_elements_list[1] += 1
            if event.type == pygame.KEYDOWN and gamestate == 1:
                #Placeholder for game over screen
                if event.key == pygame.K_r:
                    draw_menu = False
                    start_game = False
                    draw_game_over = True
                    input_name = False

                #Detect element
            
                if event.key == pygame.K_f:
                    print("Pressed: s")
                    lettuce = food_element(456, -70, "Lettuce")
                    object_order.append(lettuce)
                    object_order[-1].height = 10
                    number_elements_list[0] += 1
                if event.key == pygame.K_j:

                    print("Pressed: k")
                    tomato = food_element(480, -70, "Tomatoe")
                    object_order.append(tomato)
                    object_order[-1].height = 3
                    number_elements_list[1] += 1

                if event.key == pygame.K_d:
                    print("Pressed: d")
                    meat = food_element(460, -70, "Meat")
                    object_order.append(meat)
                    number_elements_list[2] += 1

                if event.key == pygame.K_SPACE:
                    print("Pressed: SPACE")
                    ##user wont be able to input afterwards
                    gamestate = 2
                    #Deliver order
                    # Start the timer
                    top_bread = food_element(444, -70, "Top_bun")
                    object_order.append(top_bread)
                    object_order[-1].height = 60

                    if start_time == 0:
                        start_time = pygame.time.get_ticks()
                        
                    print(number_elements_list)
                    if requested_order == number_elements_list:
                            message = show_order_delivered_message(True)
                            score_value += score_to_get(requested_order)
                            if angry_bar.angriness >=10:
                                angry_bar.angriness += -10     
                    else:
                            message = show_order_delivered_message(False)
                            if angry_bar.angriness < 100:
                                angry_bar.angriness += 10
                    show_message = True
                    requested_order = None
                    ##object_order = []
                    number_elements_list = [0,0,0]

    # Refresh and draw the menu screen
    if draw_menu:
        menu.draw()

    if start_game:
        fps.tick(30)
        ##print(fps.get_fps()) ##only use if you want the fps to be printed

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
            text_surface = order_font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (900, y))  # Adjust the position of the text
            y += 30  # Ajust the spaces between lines

        #Draw angry bar
        angry_bar.draw(screen)

        #Game over
        if angry_bar.angriness == 100:
            start_game = False
            input_name = True

        # Show the message for 2 seconds
        # Show the message for a specified duration
        if show_message:
            #Subtract to the current time the time when the spacebar was pressed
            elapsed_time = pygame.time.get_ticks() - start_time
            screen.blit(message, (10, 70))
            #Check if the time is higher than the message display time specified
            if elapsed_time >= message_display_time:
                show_message = False
                start_time = 0  # Reset the start time
                elapsed_time = 0  # Reset the elapsed time

        for i in range(len(object_order)):

            if gamestate == 3:
                object_order[i].spdx += accx

            object_order[i].spdy += gravity
            object_order[i].xPosition += object_order[i].spdx

            if object_order[i].move == True or i == 0:
                object_order[i].yPosition += object_order[i].spdy
                check_collisions(i)

            object_order[i].draw()

        if len(object_order):

            if object_order[-1].move == False and gamestate == 2:
                gamestate = 3

            if  object_order[0].xPosition > 1200 and gamestate == 3:
                object_order = []
        else: 
            bottom_bread = food_element(444, -70, "Under-bun")
            object_order.append(bottom_bread)
            object_order[0].move = False
            gamestate = 1
            
    if input_name:
            user_name = game_over.get_user_name(score_value)
            if user_name:
                print("User name: ", user_name)
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

    if draw_game_over:
        game_over.draw()

    if draw_high_scores:
        high_score.draw()


    # Refresh the screen
    pygame.display.update()