import pygame
import spritesheet
import numpy as np
import random

MAX_X_COORD = 1200
STANDING_X_COORD = 600
MOVEMENT_SPEED = 20
HEAD_SPRITES_LENGHT = 184
HEAD_SPRITES_HEIGHT = 224

cut = 0
segment_end = 2000

class the_guy_head():
    def __init__(self, body):
        self.pair = body
        self.offset = 0
        self.direction = 1
        self.sheet_x = 0
        self.animation_frame = 0
        self.state = None

    def draw(self, costume):
        if self.pair.show:
            sum_of_all_y = self.pair.y + self.offset + self.pair.offset - 204
            self.pair.screen.blit(costume,(self.pair.x - 4, sum_of_all_y))

class the_guy():
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.show = True
        self.spdx = 0
        self.spdy = 3
        self.offset = 0

    def draw(self):
        if self.show:
            self.screen.blit(pygame.image.load('images/delivery_man/delivery_neck_big.png').convert_alpha(),(self.x, self.y + self.offset))

def animation(walk_animation, body, head):

    head_sheet = spritesheet.get_spritesheet('images/delivery_man/head_ss_big.png')

    if head.state == 'blinking':
        head.animation_frame += 0.3
        head.sheet_x = np.floor(head.animation_frame) % 7
        if head.animation_frame > 7:
            head.state = None

    head_costume = head_sheet.imgat((head.sheet_x * HEAD_SPRITES_LENGHT, 0, HEAD_SPRITES_LENGHT, HEAD_SPRITES_HEIGHT))

    if walk_animation:
        if abs(body.offset) > 10:
            body.offset = -3    
        
        if abs(body.offset) < -10:
            body.offset = 3

        body.offset += body.spdy
    else:
        head.offset += 0.25 * head.direction
        if head.offset >= 5 or head.offset <= 0:
            head.direction = head.direction * -1
    
    body.draw()
    head.draw(head_costume)

def delivery(gamestate, body, head, total_time):

    global cut, segment_end
    segment = total_time - cut

    if segment >= segment_end:
        cut = total_time
        head.animation_frame = 0
        head.state = 'blinking'
        segment_end = random.randint(2000,4000)

    if gamestate == 1:
        if body.x > MAX_X_COORD:
            body.x = -200
        
        body.spdx = body.spdx * 0.8
        
        walk_animation = False

        if body.x < STANDING_X_COORD:
            body.spdx = MOVEMENT_SPEED
            walk_animation = True

        body.x += body.spdx

        animation(walk_animation, body, head)