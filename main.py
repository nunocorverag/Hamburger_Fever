import pygame
import random

#Handle music in the game
from pygame import mixer

#Import the menu screen
from menu_screen import MenuScreen
from game_over_screen import OverScreen

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption("Pantalla de Inicio")

#Menu screen object
menu = MenuScreen(screen)

#Over screen object
game_over = OverScreen(screen)

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
number_elements_list = [0,0,0,0,0]

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

#Determine if the game has finished
draw_game_over = False

#Score
score_value = 0
score_font  = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 500
scoreY = 10

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
            element_name = "Top_bun"
        elif i == 1:
            element_name = "Meat"
        elif i == 2:
            element_name = "Lettuce"
        elif i == 3:
            element_name = "Tomatoe"
        elif i == 4:
            element_name = "Under-bun"

        order_message += str(requested_order[i]) + " x " + str(element_name) + "\n"
    
    return order_message

#create customer order
def create_order():
    bottom_bread_num = 1
    meat_num = random.randint(1,3)
    lettuce_num = random.randint(0,3)
    tomato_num = random.randint(0,3)
    top_bread_num = 1
    requested_order = [bottom_bread_num, meat_num, lettuce_num, tomato_num, top_bread_num]

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
            if MenuScreen.check_exit_click(mouse_pos):
                running = False
            if MenuScreen.check_start_click(mouse_pos):
                draw_menu = False
                start_game = True
                print("Starting game...")
        if start_game:
            if event.type == pygame.KEYDOWN and gamestate == 1:
                #This checks if the key pressed is the left arrow
                if event.key == pygame.K_r:
                    draw_menu = False
                    start_game = False
                    draw_game_over = True
                if event.key == pygame.K_f:
                    print("Pressed: f")
                    bottom_bread = food_element(444, -70, "Under-bun")
                    object_order.append(bottom_bread)
                    number_elements_list[0] += 1
                if event.key == pygame.K_d:
                    print("Pressed: d")
                    meat = food_element(460, -70, "Meat")
                    object_order.append(meat)
                    number_elements_list[1] += 1
                if event.key == pygame.K_s:
                    print("Pressed: s")
                    lettuce = food_element(456, -70, "Lettuce")
                    object_order.append(lettuce)
                    object_order[-1].height = 10
                    number_elements_list[2] += 1
                if event.key == pygame.K_k:
                    print("Pressed: k")
                    tomato = food_element(480, -70, "Tomatoe")
                    object_order.append(tomato)
                    object_order[-1].height = 3
                    number_elements_list[3] += 1
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
                            if angry_bar.angriness >=10:
                                angry_bar.angriness += -10     
                    else:
                            message = show_order_delivered_message(False)
                            if angry_bar.angriness < 100:
                                angry_bar.angriness += 10
                    show_message = True
                    requested_order = None
                    ##object_order = []
                    number_elements_list = [0,0,0,0,0]

    # Refresh and draw the menu screen
    if draw_menu:
        menu.draw()

    if start_game:
        fps.tick(30)
        ##print(fps.get_fps()) ##only use if you want the fps to be printed

        screen.fill((0,0,0))
        screen.blit(background_image, (0,0))

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
            draw_game_over = True

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
            print(object_order[-1].move)

            if object_order[-1].move == False and gamestate == 2:
                gamestate = 3

            if  object_order[0].xPosition > 1200 and gamestate == 3:
                print('ok')
                object_order = []
        else: 
            bottom_bread = food_element(444, -70, "Under-bun")
            object_order.append(bottom_bread)
            object_order[0].move = False
            gamestate = 1
            
    if draw_game_over:
        user_name = game_over.get_user_name()
        if user_name:
            print("User name: ", user_name)
        game_over.draw()


    # Refresh the screen
    pygame.display.update()