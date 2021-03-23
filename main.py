import pygame
import ctypes
from pygame import *
from pygame.constants import FULLSCREEN, KEYDOWN

#without this line, pygame thinks the screen is only 1536 pixels wide, which fucks up elements whose position depends on the resolution
ctypes.windll.user32.SetProcessDPIAware()

#Initialise pygame
pygame.init()

#setting up display
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('QPuzzler')
disp_Width = display.get_width()
disp_Height = display.get_height()

#text shenanigans
pygame.font.init()
normal_Font = pygame.font.Font("square.ttf", 48)
menu_Font = pygame.font.Font("square.ttf", 192)

def draw_Text(display, text, color,font, X, Y,):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (X,Y)
    display.blit(textobj, textrect)


# main menu buttons
level_Select_Button = pygame.Rect(0,0, 400, 100)
level_Select_Button.center = (disp_Width/2,3*(disp_Height/6))
options_Button = pygame.Rect(0,0, 400, 100)
options_Button.center = (disp_Width/2,4*(disp_Height/6))
exit_Button = pygame.Rect(0,0, 400, 100)
exit_Button.center = (disp_Width/2,5*(disp_Height/6))
buttons = (level_Select_Button, options_Button, exit_Button)

#making it so the game can know the mouse's position
(mx, my) = pygame.mouse.get_pos()

#Game loops:
"""each different game "screen", so the main menu, the options page, level select, and the such, has it's own game loop, which contains the 
update and render sections, the player can move between those different game states by using buttons, which just launches the corresponding 
game loop and interrupts the current one"""
#main menu loop
def main_Menu():
    click = False #suddenly, python doesn't like it when click's value is given elsewhere,
    running = True
    while running:
        #everything that needs to be rendered:
        display.fill((255,255,255))
        for button in buttons:
            pygame.draw.rect(display, (0,0,0), button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text(display, "QPUZZLER", (0,0,0), menu_Font, disp_Width/2, disp_Height/5)
        draw_Text(display, "LEVEL SELECT", (0,0,0), normal_Font, disp_Width/2,3*(disp_Height/6))
        draw_Text(display, "OPTIONS", (0,0,0), normal_Font, disp_Width/2,4*(disp_Height/6))
        draw_Text(display, "EXIT", (0,0,0), normal_Font, disp_Width/2,5*(disp_Height/6))
        pygame.display.update()

        #the interactive bits, events and what to when they occur
        #the bit that checks if the mouse touches a button when it's clicked
        if click:
            if exit_Button.collidepoint(mx,my):
                level_Select(display)
            if exit_Button.collidepoint(mx,my):
                options_Menu()
            if exit_Button.collidepoint(mx,my):
                running = False
        #the bit that takes care of the different events
        click = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True #this one here is the important one
    pygame.quit()

def level_Select(display):
    pass

def options_Menu():
    pass

#runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_Menu()
