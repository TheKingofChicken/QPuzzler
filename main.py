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

fontdict = {
    "menu" : menu_Font,
    "normal" : normal_Font
}

def draw_Text(text, color,font, X, Y,):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (X,Y)
    display.blit(textobj, textrect)


# main menu buttons
level_Select_Button = pygame.Rect(0,0, 400, 100)
level_Select_Button.center = (disp_Width/2,3*disp_Height/6)
options_Button = pygame.Rect(0,0, 400, 100)
options_Button.center = (disp_Width/2,4*disp_Height/6)
exit_Button = pygame.Rect(0,0, 400, 100)
exit_Button.center = (disp_Width/2,5*disp_Height/6)
main_Menu_Buttons = (level_Select_Button, options_Button, exit_Button)

#options buttons
back_Button = pygame.Rect(0,0,200,100)
back_Button.center = (disp_Width/5,7*disp_Height/8)
apply_Button = pygame.Rect(0,0,200,100)
apply_Button.center = (4*disp_Width/5, 7* disp_Height/8)
option_Buttons = (back_Button, apply_Button)

#level select buttons
#includes back_button
start_Button = pygame.Rect(0,0,200,100)
start_Button.center = (4*disp_Width/5, 7* disp_Height/8)
level_Select_Buttons = (back_Button, start_Button)

#colors we're actually gonna use
white = (255,255,255)
black=(0,0,0)

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
        display.fill(white)
        for button in main_Menu_Buttons:
            pygame.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("QPUZZLER", black, fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_Text("LEVEL SELECT", black, fontdict["normal"], disp_Width/2,3*disp_Height/6)
        draw_Text("OPTIONS", black, fontdict["normal"], disp_Width/2,4*disp_Height/6)
        draw_Text("EXIT", black, fontdict["normal"], disp_Width/2,5*disp_Height/6)
        pygame.display.update()

        #the interactive bits, events and what to when they occur, (update section)
        #the bit that checks if the mouse touches a button when it's clicked
        if click:
            if level_Select_Button.collidepoint(mx,my):
                level_Select(display)
            if options_Button.collidepoint(mx,my):
                options_Menu(display)
            if exit_Button.collidepoint(mx,my):
                running = False
        #the bit that takes care of the different events
        click = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pygame.mouse.get_pos()
                    click = True #this one here is the important one
    pygame.quit()

def level_Select(display):
    
    click = False
    running = True

    while running:
        #render section
        display.fill(white)
        for button in level_Select_Buttons:
            pygame.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("BACK", black, fontdict["normal"],disp_Width/5,7*disp_Height/8)
        draw_Text("START", black, fontdict["normal"],4*disp_Width/5, 7* disp_Height/8)
        pygame.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx,my)):
                running = False
            if start_Button.collidepoint((mx,my)):
                level()
        #events
        click = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pygame.mouse.get_pos()
                    click = True #this one here is the important one


def options_Menu(display):

    def apply_Settings():
            pass
    
    click = False
    running = True
    
    while running :
        #render section
        display.fill(white)
        for button in option_Buttons:
            pygame.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("OPTIONS", black, fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_Text("BACK", black, fontdict["normal"],disp_Width/5,7*disp_Height/8)
        draw_Text("APPLY", black, fontdict["normal"],4*disp_Width/5,7*disp_Height/8)
        pygame.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx,my)):
                running = False
            if apply_Button.collidepoint((mx,my)):
                apply_Settings()
                running = False
        #events
        click = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pygame.mouse.get_pos()
                    click = True #this one here is the important one

def level():
    pass #placeholder

#runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_Menu()
