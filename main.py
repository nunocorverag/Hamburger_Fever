import pygame
import math
import random

#Initialize the game
pygame.init()

#Set up the screen dimensions
screen = pygame.display.set_mode((800,600))

#Background
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))

#Delivered order text
delivered_font = pygame.font.Font("freesansbold.ttf", 20)

class food_element:
    def __init__(self, x, y, food_name):
        self.xPosition = x
        self.yPosition = y
        self.food_name = food_name
        self.image = None
    
    def draw(self):
        if self.food_name == "bottom_bread":
            self.image = pygame.image.load("images/food/bottom_bread.png")
        elif self.food_name == "meat":
            self.image = pygame.image.load("images/food/meat.png")
        elif self.food_name == "lettuce":
            self.image = pygame.image.load("images/food/lettuce.png")
        elif self.food_name == "tomato":
            self.image = pygame.image.load("images/food/tomato.png")
        elif self.food_name == "top_bread":
            self.image = pygame.image.load("images/food/top_bread.png")

        self.image = pygame.transform.scale(self.image, (100,100))

        screen.blit(self.image, (self.xPosition, self.yPosition))

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

#deliver order
deliver_order = False

#Initial speed of falling objects, it will increase as there are more objects, since the refresh gets slower as adding new objects
base_speed = 0.2

object_order = []

#This array will get the number of each element
#   bottom_bread -> 0
#   meat -> 1
#   lettuce -> 2
#   tomato -> 3
#   top_bread -> 4
number_elements_list = [0,0,0,0,0]

#Customer order
requested_order = [1,1,1,2,1]

running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background_image, (0,0))

    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #This checks if the key pressed is the left arrow
            if event.key == pygame.K_f:
                print("Pressed: f")
                bottom_bread = food_element(350, -70, "bottom_bread")
                object_order.append(bottom_bread)
                number_elements_list[0] += 1
            if event.key == pygame.K_d:
                print("Pressed: d")
                meat = food_element(350, -70, "meat")
                object_order.append(meat)
                number_elements_list[1] += 1
            if event.key == pygame.K_s:
                print("Pressed: s")
                lettuce = food_element(350, -70, "lettuce")
                object_order.append(lettuce)
                number_elements_list[2] += 1
            if event.key == pygame.K_k:
                print("Pressed: k")
                tomato = food_element(350, -70, "tomato")
                object_order.append(tomato)
                number_elements_list[3] += 1
            if event.key == pygame.K_j:
                print("Pressed: j")
                top_bread = food_element(350, -70, "top_bread")
                object_order.append(top_bread)
                number_elements_list[4] += 1
            if event.key == pygame.K_SPACE:
                print("Pressed: SPACE")
                #Deliver order
                if requested_order == object_order:
                        message = show_order_delivered_message(True)
                else:
                        message = show_order_delivered_message(False)
                screen.blit(message, (150, 50))

    num_objects = len(object_order)

    #NOTE: IDK I used this formula to solve the speed problem
    speed = base_speed * num_objects

    for i in range(len(object_order)):
        object_order[i].draw()
        if i == 0:        
            if object_order[i].yPosition < 500:
                object_order[i].yPosition += speed
        else:
            if not isCollision(object_order[i].xPosition, object_order[i].yPosition, object_order[i - 1].xPosition, object_order[i - 1].yPosition):
                object_order[i].yPosition += speed

    print(number_elements_list)
    #Update the display
    pygame.display.update() 