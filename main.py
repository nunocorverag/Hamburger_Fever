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

class food_element:
    def __init__(self, x, y, food_name):
        self.xPosition = x
        self.yPosition = y
        self.food_name = food_name
        self.image = None
    
    def draw(self):
        if self.food_name == "bottom_bread":
            self.image = pygame.image.load("images/food/bottom_bread.png")
        elif self.food_name == "top_bread":
            self.image = pygame.image.load("images/food/top_bread.png")
        self.image = pygame.transform.scale(self.image, (100,100))

        screen.blit(self.image, (self.xPosition, self.yPosition))

def isCollision(object2_x, object2_y, object1_x, object1_y):
    # Distance between two points D = sqrt*(x2 - x1)^2 + (y2 - y1)^2)
    distance = math.sqrt(math.pow(object2_x - object1_x,2) + math.pow(object2_y - object1_y,2))
    if (distance < 27):
        return True
    else:
        return False

object_order = []

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
                pressed_f = True
                bottom_bread = food_element(350, -70, "bottom_bread")
                object_order.append(bottom_bread)
            if event.key == pygame.K_j:
                print("Pressed: j")
                pressed_j = True
                top_bread = food_element(350, -70, "top_bread")
                object_order.append(top_bread)


    for i in range(len(object_order)):
        object_order[i].draw()
        if i == 0:        
            if object_order[i].yPosition < 500:
                object_order[i].yPosition += 0.2
        else:
            if not isCollision(object_order[i].xPosition, object_order[i].yPosition, object_order[i - 1].xPosition, object_order[i - 1].yPosition):
                object_order[i].yPosition += 0.2

    #Update the display
    pygame.display.update() 