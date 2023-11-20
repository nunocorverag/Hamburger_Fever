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
        self.offset = 1
        self.direction = 1
        self.sheet_x = 0
        self.sheet_y = 0
        self.animation_frame = 0
        self.state = None
        self.talk_time = 0

    def draw(self, costume):
        if self.pair.show:
            sum_of_all_x = self.pair.x - self.pair.camera_x - 4
            sum_of_all_y = self.pair.y - self.pair.camera_y + self.offset + self.pair.offset - 204
            self.pair.screen.blit(costume,(sum_of_all_x, sum_of_all_y))

class the_guy():
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.show = True
        self.spdx = 0
        self.spdy = 3
        self.offset = 0
        self.camera_x = 0
        self.camera_y = 0

    def draw(self):
        if self.show:
            torso_image = pygame.image.load('images/delivery_man/chunky_body.png').convert_alpha()
            self.screen.blit(torso_image, (self.x - self.camera_x, self.y - self.camera_y + self.offset))

    def get_camera(self, camera_x, camera_y):
        self.camera_x = camera_x * 0.6
        self.camera_y = camera_y * 0.6

##############################################################################################################################################

def get_camera(body, camera_x, camera_y):
    body.get_camera(camera_x, camera_y)

def send_changes_in_gamestate():
    return to_return

def animation(walk_animation, body, head):

    head_sheet = spritesheet.get_spritesheet('images/delivery_man/head_ss_big.png')
    if head.state == 'talking':
        head.animation_frame += 0.3
        head.sheet_x = np.floor(head.animation_frame) % 5
        head.sheet_y = 1
        head.offset = 8

        if head.animation_frame % 5 == 0:
            head.animation_frame = 0

    else:

        if head.state == 'blinking':
            head.animation_frame += 0.3
            head.sheet_x = np.floor(head.animation_frame) % 7
            head.sheet_y = 0
            if head.animation_frame > 7:
                head.state = None  

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
        
    head_costume = head_sheet.imgat((head.sheet_x * HEAD_SPRITES_LENGHT, head.sheet_y * HEAD_SPRITES_HEIGHT, HEAD_SPRITES_LENGHT, HEAD_SPRITES_HEIGHT))

    body.draw()
    head.draw(head_costume)

##############################################################################################################################################

def delivery(gamestate, body, head, total_time):

    global cut, segment_end, to_return
    to_return = None

    segment = total_time - cut
    max_talk_time = 70

    if head.state != 'blinking': head.state = None
    walk_animation = False

    body.spdx = body.spdx * 0.8

    if gamestate == 4:

        if body.x < STANDING_X_COORD:
            body.spdx = MOVEMENT_SPEED
            walk_animation = True
        else:
            to_return = 5

    elif gamestate == 5:
        if head.talk_time < max_talk_time:
            head.state = 'talking'
        else:
            to_return = 6
        
    elif gamestate == 6:
        head.offset = 1
        to_return = 3

    elif gamestate == 7:

        body.spdx = MOVEMENT_SPEED
        walk_animation = True
        
        if body.x > MAX_X_COORD:
            body.x = -200
            to_return = 4
        

    if segment >= segment_end and head.state != 'talking':
        cut = total_time
        head.animation_frame = 0
        head.state = 'blinking'
        segment_end = random.randint(2000, 4000)
    elif head.state == 'talking':
        head.talk_time += 1 
    else:
        head.talk_time = 0

    body.x += body.spdx

    animation(walk_animation, body, head)