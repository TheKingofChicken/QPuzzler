
#This whole file is extremely wip, probably not gonna be there in the finished product
import pygame
from pygame import display

class Entity: #with the artstyle we're going with, we probably won't even need sprites, maybe only for the qubits
    def __init__(self, height, width, sprite, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.height = height
        self.width = width
        self.sprite = sprite

def Draw_Text(display, text, color,font, X, Y,):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    display.blit(textobj, (X,Y))

normal_Font = pygame.font.Font("Pixel_Font.ttf", 21)
menu_Font = pygame.font.Font("Pixel_Font.ttf", 35)