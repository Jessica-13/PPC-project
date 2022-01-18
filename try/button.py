#!/usr/bin/env python3

# Exemple button 

import pygame
import sys


# initializing the constructor
pygame.init()

# screen resolution
res = (1380,868)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255,255,255)

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel',35)

# rendering a text written in
# this font
text = smallfont.render('quit' , True , color)

# *******************************************************************
class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__() 
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, color, (25, 25), 25)
        self.click_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.click_image, color, (25, 25), 25)
        pygame.draw.circle(self.click_image, (255, 255, 255), (25, 25), 25, 4)
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = (x, y))
        self.clicked = False

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked

        self.image = self.click_image if self.clicked else self.original_image
    



clock = pygame.time.Clock()

sprite_object = SpriteObject(*screen.get_rect().center, (128, 128, 0))
group = pygame.sprite.Group([
    SpriteObject(screen.get_width() // 3, screen.get_height() // 3, (128, 0, 0)),
    SpriteObject(screen.get_width() * 2 // 3, screen.get_height() // 3, (0, 128, 0)),
    SpriteObject(screen.get_width() // 3, screen.get_height() * 2 // 3, (0, 0, 128)),
    SpriteObject(screen.get_width() * 2// 3, screen.get_height() * 2 // 3, (128, 128, 0)),
])
# *******************************************************************

if __name__ == '__main__':
    while True:
        
        for ev in pygame.event.get():
            
            if ev.type == pygame.QUIT:
                pygame.quit()
                
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                
                #if the mouse is clicked on the
                # button the game is terminated
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    pygame.quit()
                    
        # fills the screen with a color
        screen.fill((60,25,60))
        
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        
        # if mouse is hovered on a button it
        # changes to lighter shade
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
            pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
            
        else:
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])
        
        # superimposing the text onto our button
        screen.blit(text , (width/2+50,height/2))
        
        # updates the frames of the game
        # pygame.display.update()
    
        clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False 

        group.update(event_list)

        screen.fill(0)
        group.draw(screen)
        pygame.display.flip()

pygame.quit()
exit()
      