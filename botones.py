import pygame
class button():
    def __init__(self,x,y,image,scale,screen): #Cuando se usa pygame todo es con imágenes, primero la imágen y luego se importa, incluso el texto.
        width=image.get_width()
        height=image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))#Para pixeles solo se trabaja con float
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y) #A partir de estas coordenadas se crea el botón
        self.screen = screen

    def check_clicked_button(self, mouse_pos):
        #Ver posición del mouse
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self):
        #impresión imágen
        self.screen.blit(self.image, (self.rect.x, self.rect.y)) 
