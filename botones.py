import pygame
class button():
    def _init_(self,x,y,image,scale): #Cuando se usa pygame todo es con imágenes, primero la imágen y luego se importa, incluso el texto.
        width=image.get_width()
        height=image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))#Para pixeles solo se trabaja con float
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y) #A partir de estas coordenadas se crea el botón
    def draw(self, surface):
        action = False
        #Ver posición del mouse
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and (self.clicked==False):
                self.clicked=True
                action = True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False
        #impresión imágen
        surface.blit(self.image, (self.rect.x, self.rect.y)) 

        return action