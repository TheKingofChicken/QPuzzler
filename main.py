import pygame as pg
import ctypes
import Circuit_Logic as cl

#without this line, pygame thinks the screen is only 1536 pixels wide, which fucks up elements whose position depends on the resolution
ctypes.windll.user32.SetProcessDPIAware()

#Initialise pygame
pg.init()

#setting up display
display = pg.display.set_mode((0,0),pg.FULLSCREEN)
pg.display.set_caption('QPuzzler')
disp_Width = display.get_width()
disp_Height = display.get_height()
fps_Limiter = pg.time.Clock()

#text shenanigans
pg.font.init()
normal_Font = pg.font.Font("square.ttf", 48)
menu_Font = pg.font.Font("square.ttf", 192)

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
level_Select_Button = pg.Rect(0,0, 400, 100)
level_Select_Button.center = (disp_Width/2,3*disp_Height/6)
options_Button = pg.Rect(0,0, 400, 100)
options_Button.center = (disp_Width/2,4*disp_Height/6)
exit_Button = pg.Rect(0,0, 400, 100)
exit_Button.center = (disp_Width/2,5*disp_Height/6)
main_Menu_Buttons = (level_Select_Button, options_Button, exit_Button)

#options buttons
back_Button = pg.Rect(0,0,200,100)
back_Button.center = (disp_Width/5,7*disp_Height/8)
apply_Button = pg.Rect(0,0,200,100)
apply_Button.center = (4*disp_Width/5, 7* disp_Height/8)
option_Buttons = (back_Button, apply_Button)

#level select buttons
#includes back_button
start_Button = pg.Rect(0,0,200,100)
start_Button.center = (4*disp_Width/5, 7* disp_Height/8)
level_Select_Buttons = (back_Button, start_Button)

#colors we're actually gonna use
white = (255,255,255)
black=(0,0,0)
grey = (200,200,200)

#levels:
gate = cl.H_Gate(0,0,0,0)
gate2 = cl.H_Gate(0,0,0,0)
track = cl.Track(0)
track2 = cl.Track(0)
track.Add_Gate(gate)
track.Add_Gate(gate2)
current_level = cl.Level([],[])
current_level.Add_Track(track)
current_level.Add_Track(track2)

#Game loops:
"""each different game "screen", so the main menu, the options page, level select, and the such, has it's own game loop, which contains the 
update and render sections, the player can move between those different game states by using buttons, which just launches the corresponding 
game loop and interrupts the current one"""
#main menu loop
def main_Menu():
    click = False #suddenly, python doesn't like it when click's value is given elsewhere,
    running = True
    while running:
        fps_Limiter.tick(60)
        #everything that needs to be rendered:
        display.fill(white)
        for button in main_Menu_Buttons:
            pg.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("QPUZZLER", black, fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_Text("LEVEL SELECT", black, fontdict["normal"], disp_Width/2,3*disp_Height/6)
        draw_Text("OPTIONS", black, fontdict["normal"], disp_Width/2,4*disp_Height/6)
        draw_Text("EXIT", black, fontdict["normal"], disp_Width/2,5*disp_Height/6)
        pg.display.update()

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
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pg.mouse.get_pos()
                    click = True #this one here is the important one
    pg.quit()

def level_Select(display):
    
    click = False
    running = True

    while running:
        fps_Limiter.tick(60)
        #render section
        display.fill(white)
        for button in level_Select_Buttons:
            pg.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("BACK", black, fontdict["normal"],disp_Width/5,7*disp_Height/8)
        draw_Text("START", black, fontdict["normal"],4*disp_Width/5, 7* disp_Height/8)
        pg.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx,my)):
                running = False
            if start_Button.collidepoint((mx,my)):
                Level(display, current_level)
        #events
        click = False
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pg.mouse.get_pos()
                    click = True #this one here is the important one


def options_Menu(display):

    def apply_Settings():
            pass
    
    click = False
    running = True
    
    while running :
        fps_Limiter.tick(60)
        #render section
        display.fill(white)
        for button in option_Buttons:
            pg.draw.rect(display, black, button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_Text("OPTIONS", black, fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_Text("BACK", black, fontdict["normal"],disp_Width/5,7*disp_Height/8)
        draw_Text("APPLY", black, fontdict["normal"],4*disp_Width/5,7*disp_Height/8)
        pg.display.update()

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
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pg.mouse.get_pos()
                    click = True #this one here is the important one

def Level(display, level):
    running = True
    #eveyrthing after this is given a value during the update section, its just given one at the start here so the first render section stop whyning
    holding = False
    held_rectangle = None
    (mx,my) = (0,0)
    for track in level.tracks:# creates a rectangle for every track and gate
        track.rectangle = pg.Rect(430,0, 1480, 150)
        for gate in track.gates:
            gate.rectangle = pg.Rect(0,0, 100, 100)
    
    #game loop
    while running:
        fps_Limiter.tick(60)
        track_Rectangle_Y = 10
        #render section
        display.fill(white)
        for track in level.tracks:
            if track is held_rectangle: #skips the whole positioning code if the track is the one currently being moved
                pg.draw.rect(display, grey, track.rectangle, 10)
                continue
            track.rectangle.y = track_Rectangle_Y
            if held_rectangle in level.tracks:
                if track.rectangle.inflate((10,10)).collidepoint((mx,my)):
                    track_Rectangle_Y += 160
                    track.rectangle.y += 160
            pg.draw.rect(display, grey, track.rectangle, 10)
            track_Rectangle_Y += 160 #offsets the position for the next track to be drawn below this current one
        #here the code is pretty much exactly repeted, except that it positions the gates on the track, and makes the gates follow the track
        for track in level.tracks:
            gate_Rectangle_X = track.rectangle.x + 117
            for gate in track.gates:
                if gate is held_rectangle:#skips the whole positioning code if the gate is the one being currently held
                    pg.draw.rect(display, black, gate.rectangle)
                    continue
                gate.rectangle.center = (gate_Rectangle_X, track.rectangle.centery)
                pg.draw.rect(display, black, gate.rectangle)
                gate_Rectangle_X+=125
        pg.draw.rect(display, white, pg.Rect(10, 890, 1900, 300))
        pg.draw.rect(display, black, pg.Rect(10, 890, 1900, 300), 10)
        pg.draw.rect(display, white, pg.Rect(10, 10, 400, 860))
        pg.draw.rect(display, black, pg.Rect(10, 10, 400, 860), 10)
        pg.display.update()

        #update section
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rectangle_is_gate = False
                    (mx, my) = pg.mouse.get_pos()
                    for track in level.tracks:
                        for gate in track.gates:
                            if gate.rectangle.collidepoint(mx,my):
                                holding = True
                                held_rectangle = gate
                                rectangle_is_gate = True
                                break
                        if rectangle_is_gate:
                            break
                        if track.rectangle.collidepoint(mx,my):
                            holding = True
                            held_rectangle = track
                            break
            if event.type == pg.MOUSEBUTTONUP:
                holding = False
                held_rectangle = None
            if holding :
                (mx, my) = pg.mouse.get_pos()
                if held_rectangle in level.tracks:
                    held_rectangle.rectangle.centery = my
                else :held_rectangle.rectangle.center = (mx,my)

#runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_Menu()
