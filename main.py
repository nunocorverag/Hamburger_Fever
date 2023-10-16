import pygame
import math
import random
import botones

#Handle music in the game
from pygame import mixer

#Import the menu screen
from menu_screen import MenuScreen

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption("Pantalla de Inicio")

#Menu screen object
menu = MenuScreen(screen)

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

#Initial speed of falling objects, it will increase as there are more objects, since the refresh gets slower as adding new objects
base_speed = 4

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

#Initialize requested order variable
requested_order = None

#Determine if the menu has to be drawn or no
draw_menu = True

#Determine if the game is started
start_game = False

class food_element():
    def __init__(self, x, y, food_name):
        self.xPosition = x
        self.yPosition = y
        self.food_name = food_name
        self.image = None
    
    def draw(self):
        self.image = pygame.image.load("images/food/" + self.food_name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
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

def isCollision(object2_x, object2_y, object1_x, object1_y):
    # Distance between two points D = sqrt*(x2 - x1)^2 + (y2 - y1)^2)
    distance = math.sqrt(math.pow(object2_x - object1_x,2) + math.pow(object2_y - object1_y,2))
    if (distance < 25):
        return True
    else:
        return False

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
            element_name = "top bread"
        elif i == 1:
            element_name = "meat"
        elif i == 2:
            element_name = "lettuce"
        elif i == 3:
            element_name = "tomato"
        elif i == 4:
            element_name = "bottom bread"

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
            if event.type == pygame.KEYDOWN:
                #This checks if the key pressed is the left arrow
                if event.key == pygame.K_f:
                    print("Pressed: f")
                    bottom_bread = food_element(490, -70, "bottom_bread")
                    object_order.append(bottom_bread)
                    number_elements_list[0] += 1
                if event.key == pygame.K_d:
                    print("Pressed: d")
                    meat = food_element(490, -70, "meat")
                    object_order.append(meat)
                    number_elements_list[1] += 1
                if event.key == pygame.K_s:
                    print("Pressed: s")
                    lettuce = food_element(490, -70, "lettuce")
                    object_order.append(lettuce)
                    number_elements_list[2] += 1
                if event.key == pygame.K_k:
                    print("Pressed: k")
                    tomato = food_element(490, -70, "tomato")
                    object_order.append(tomato)
                    number_elements_list[3] += 1
                if event.key == pygame.K_j:
                    print("Pressed: j")
                    top_bread = food_element(490, -70, "top_bread")
                    object_order.append(top_bread)
                    number_elements_list[4] += 1
                if event.key == pygame.K_SPACE:
                    print("Pressed: SPACE")
                    #Deliver order
                    # Start the timer
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
                    object_order = []
                    number_elements_list = [0,0,0,0,0]

    # Refresh and draw the menu screen
    if draw_menu:
        menu.draw()

    if start_game:
        fps.tick(30)

        screen.fill((0,0,0))
        screen.blit(background_image, (0,0))

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
            game_over_text()

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

        #NOTE: IDK I used this formula to solve the speed problem
        # num_objects = len(object_order)
        speed = base_speed

        for i in range(len(object_order)):
            object_order[i].draw()
            if i == 0:        
                if object_order[i].yPosition < 550:
                    object_order[i].yPosition += speed
            else:
                if not isCollision(object_order[i].xPosition, object_order[i].yPosition, object_order[i - 1].xPosition, object_order[i - 1].yPosition):
                    object_order[i].yPosition += speed

    # Refresh the screen
    pygame.display.update()