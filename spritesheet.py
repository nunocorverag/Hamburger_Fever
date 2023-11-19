import pygame

def imgcolorkey(image):
    transColor = (0, 0, 0)
    image.set_colorkey(transColor)
    return image

class get_spritesheet():
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise message
        
    def imgat(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return imgcolorkey(image)