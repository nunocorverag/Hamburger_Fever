import pygame

MAX_X_COORD = 1200
STANDING_X_COORD = 600
MOVEMENT_SPEED = 30


class the_guy():
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.show = True
        self.spdx = 0
        self.spdy = 0
        self.offset = 0

    def draw(self):
        if self.show:
            image = pygame.image.load('images/delivery_man/delivery_neck_big.png').convert_alpha()
            self.screen.blit(image,(self.x, self.y))

def animation(walk_animation, body):
    if walk_animation:

        if abs(body.offset) > 10:
            body.spdy = -3
        
        if abs(body.offset) < -10:
            body.spdy = 3

        body.offset += body.spdy
        body.y += body.spdy
    else:
        None

def delivery(gamestate, body):

    if gamestate == 1:
        if body.x > MAX_X_COORD:
            body.x = -200
        
        body.spdx = body.spdx * 0.8
        
        walk_animation = False

        if body.x < STANDING_X_COORD:
            body.spdx = MOVEMENT_SPEED
            walk_animation = True

        body.x += body.spdx

        animation(walk_animation, body)

    body.draw()