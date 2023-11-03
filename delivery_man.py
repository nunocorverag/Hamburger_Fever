import pygame

class the_guy():
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        image = pygame.image.load('images/delivery_man/delivery_neck_big.png').convert_alpha()
        self.screen.blit(image,(self.x, self.y))

def delivery(gamestate, me):
    me.draw()