import pygame as pg
import ctypes
import Circuit_Logic as cl

# without this line, pygame thinks the screen is only 1536 pixels wide, which fucks up elements whose position depends on the resolution
ctypes.windll.user32.SetProcessDPIAware()

# Initialise pygame
pg.init()

# setting up display
display = pg.display.set_mode((1920, 1200))
pg.display.set_caption('QPuzzler')
disp_Width = display.get_width()
disp_Height = display.get_height()
fps_Limiter = pg.time.Clock()

# text shenanigans
pg.font.init()
normal_Font = pg.font.Font("square.ttf", 48)
menu_Font = pg.font.Font("square.ttf", 192)
fontdict = {
    "menu" : menu_Font, 
    "normal" : normal_Font
}

def draw_text(display, text, color, font, X, Y, ):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (X, Y)
    display.blit(textobj, textrect)

# colors we're actually gonna use
colordict = {
    "white" : (255, 255, 255), 
    "black" : (0, 0, 0), 
    "grey" : (150, 150, 150), 
    "blue" : (0, 137, 255), 
    "red" : (255, 50, 50), 
    "yellow" : (240, 240, 50)
    }

# Things to draw the gates
gatedict = {
    "H" : colordict["blue"], 
    "X" : colordict["red"], 
    "T" : colordict["yellow"]
}

def draw_gate(gate):
    if str(gate) == "I":
        return ""
    pg.draw.rect(display, gatedict[str(gate)], gate.rectangle)
    pg.draw.rect(display, colordict["black"], gate.rectangle, 10)
    draw_text(display, str(gate), colordict["white"], fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)

# main menu buttons
level_Select_Button = pg.Rect(0, 0, 400, 100)
level_Select_Button.center = (disp_Width/2, 3*disp_Height/6)
options_Button = pg.Rect(0, 0, 400, 100)
options_Button.center = (disp_Width/2, 4*disp_Height/6)
exit_Button = pg.Rect(0, 0, 400, 100)
exit_Button.center = (disp_Width/2, 5*disp_Height/6)
main_Menu_Buttons = (level_Select_Button, options_Button, exit_Button)

# options buttons
back_Button = pg.Rect(0, 0, 200, 100)
back_Button.center = (disp_Width/5, 7*disp_Height/8)
apply_Button = pg.Rect(0, 0, 200, 100)
apply_Button.center = (4*disp_Width/5, 7* disp_Height/8)
option_Buttons = (back_Button, apply_Button)

# level select buttons
# includes back_button
start_Button = pg.Rect(0, 0, 200, 100)
start_Button.center = (4*disp_Width/5, 7* disp_Height/8)
level_Select_Buttons = (back_Button, start_Button)

# levels:
base_Gates = [cl.H_Gate(0, 0, 0, 0), cl.X_Gate(0, 0, 0, 0)]
gate = cl.H_Gate(0, 0, 0, 0)
gate2 = cl.X_Gate(0, 0, 0, 0)
gate3 = cl.T_Gate(0, 0, 0, 0)
track = cl.Track(0)
track2 = cl.Track(0)
track3 = cl.Track(0)
track.gates.append(gate)
gate.current_Track = track
track.gates.append(gate2)
gate2.current_Track = track
track2.gates.append(gate3)
gate3.current_Track = track2
current_level = cl.Level([], [])
current_level.add_track(track)
current_level.add_track(track2)
current_level.add_track(track3)
# Game loops:
"""each different game "screen", so the main menu, the options page, level select, and the such, has it's own game loop, which contains the 
update and render sections, the player can move between those different game states by using buttons, which just launches the corresponding 
game loop and interrupts the current one"""
# main menu loop
def main_menu():
    click = False #suddenly, python doesn't like it when click's value is given elsewhere, 
    running = True
    while running:
        fps_Limiter.tick(60)
        #everything that needs to be rendered:
        display.fill(colordict["white"])
        for button in main_Menu_Buttons:
            pg.draw.rect(display, colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_text(display, "QPUZZLER", colordict["black"], fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_text(display, "LEVEL SELECT", colordict["black"], fontdict["normal"], disp_Width/2, 3*disp_Height/6)
        draw_text(display, "OPTIONS", colordict["black"], fontdict["normal"], disp_Width/2, 4*disp_Height/6)
        draw_text(display, "EXIT", colordict["black"], fontdict["normal"], disp_Width/2, 5*disp_Height/6)
        pg.display.update()

        #the interactive bits, events and what to when they occur, (update section)
        #the bit that checks if the mouse touches a button when it's clicked
        if click:
            if level_Select_Button.collidepoint(mx, my):
                level_select(display)
            if options_Button.collidepoint(mx, my):
                options_menu(display)
            if exit_Button.collidepoint(mx, my):
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

def level_select(display):
    
    click = False
    running = True

    while running:
        fps_Limiter.tick(60)
        #render section
        display.fill(colordict["white"])
        for button in level_Select_Buttons:
            pg.draw.rect(display, colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_text(display, "BACK", colordict["black"], fontdict["normal"], disp_Width/5, 7*disp_Height/8)
        draw_text(display, "START", colordict["black"], fontdict["normal"], 4*disp_Width/5, 7* disp_Height/8)
        pg.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx, my)):
                running = False
            if start_Button.collidepoint((mx, my)):
                level(display, current_level)
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


def options_menu(display):

    def apply_settings():
            pass
    
    click = False
    running = True
    
    while running :
        fps_Limiter.tick(60)
        #render section
        display.fill(colordict["white"])
        for button in option_Buttons:
            pg.draw.rect(display, colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        draw_text(display, "OPTIONS", colordict["black"], fontdict["menu"], disp_Width/2, disp_Height/5)
        draw_text(display, "BACK", colordict["black"], fontdict["normal"], disp_Width/5, 7*disp_Height/8)
        draw_text(display, "APPLY", colordict["black"], fontdict["normal"], 4*disp_Width/5, 7*disp_Height/8)
        pg.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx, my)):
                running = False
            if apply_Button.collidepoint((mx, my)):
                apply_settings()
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

def level(display, level):
    running = True
    #eveyrthing after this is given a value during the update section, its just given one at the start here so the first render section stop whyning
    holding = False
    held_rectangle = None
    base_Gate_Rectangle_Y = 1010
    base_Gate_Rectangle_X = 30
    track_Rectangle_Y = 10
    track_Rectangle_X = 420
    (mx, my) = (0, 0)
    old_mouse_pos = (0,0)
    
    #game loop
    while running:
        fps_Limiter.tick(60)
        #render and positionnement section
        display.fill(colordict["white"])
        for track in level.tracks:
            for gate in track.gates:
                if gate is held_rectangle:#skips the whole positioning code if the gate is the one being currently held
                    continue
                gate.rectangle.center = (track.rectangle.x + (125*(1+track.gates.index(gate))), track.rectangle.centery)
                draw_gate(gate)
                draw_text(display, str(gate), colordict["black"], fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
                if isinstance(held_rectangle, cl.Quantum_Gate):
                    new_gate_pos = round((mx - 555)/125)
                    if track != held_rectangle.current_Track:
                        if track.rectangle.collidepoint((mx, my)):
                            track.move_gate(new_gate_pos, held_rectangle)
                    elif held_rectangle.current_Track.gates.index(held_rectangle) != new_gate_pos:
                        held_rectangle.current_Track.gates.pop(held_rectangle.current_Track.gates.index(held_rectangle))
                        track.gates.insert(new_gate_pos, held_rectangle)
            if track is held_rectangle: #skips the whole positioning code if the track is the one currently being moved
                pg.draw.rect(display, colordict["grey"], track.rectangle, 10)
                for gate in track.gates:
                    gate.rectangle.center = (track.rectangle.x + (125*(1+track.gates.index(gate))), track.rectangle.centery)
                continue
            if isinstance(held_rectangle, cl.Track):#everything inside this if is to change the position of the track when it is dropped
                if track.rectangle.inflate((11, 11)).collidepoint((mx, my)):
                    if level.tracks.index(held_rectangle) < level.tracks.index(track):
                        offset = 1
                    else: offset = 0
                    level.move_track(level.tracks.index(track)+offset,held_rectangle)
            track.rectangle.y = track_Rectangle_Y + (160 * level.tracks.index(track))
            track.rectangle.x = track_Rectangle_X
            pg.draw.rect(display, colordict["grey"], track.rectangle, 10)
        #here the code is pretty much exactly repeted, except that it positions the gates on the track, and makes the gates follow the track
        pg.draw.rect(display, colordict["white"], pg.Rect(10, disp_Height-210, disp_Width-20, 200))
        pg.draw.rect(display, colordict["black"], pg.Rect(10, disp_Height-210, disp_Width-20, 200), 10)
        pg.draw.rect(display, colordict["white"], pg.Rect(10, 10, 400, disp_Height-240))
        pg.draw.rect(display, colordict["black"], pg.Rect(10, 10, 400, disp_Height-240), 10)
        for gate in base_Gates:
            if gate is held_rectangle:
                draw_gate(gate)
                continue
            gate.rectangle.x = base_Gate_Rectangle_X + (125 * base_Gates.index(gate))
            gate.rectangle.y = base_Gate_Rectangle_Y
            draw_gate(gate)
        if held_rectangle and held_rectangle not in level.tracks:
            draw_gate(held_rectangle)
        pg.display.update()
                
        #update section
        (mx, my) = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type is pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rectangle_is_gate = False
                    for track in level.tracks:
                        for gate in track.gates:
                            if gate.rectangle.collidepoint(mx, my):
                                holding = True
                                held_rectangle = gate
                                rectangle_is_gate = True
                                break
                        if rectangle_is_gate:
                            break
                        if track.rectangle.collidepoint(mx, my):
                            holding = True
                            held_rectangle = track
                            break
                    for gate in base_Gates:
                        if gate.rectangle.collidepoint(mx, my):
                            holding = True
                            held_rectangle = gate
                            break
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if isinstance(held_rectangle, cl.Quantum_Gate):
                        for track in level.tracks:
                            if track.rectangle.collidepoint((mx, my)):
                                new_Gate_pos = round((mx - 555)/125)
                                if len(track.gates) < new_Gate_pos:
                                    held_rectangle.current_Track.gates.pop(held_rectangle.current_Track.gates.index(held_rectangle))
                                    for x in range(new_Gate_pos-len(track.gates)):
                                        temp_gate = cl.I_Gate(0, 0, 0, 0)
                                        temp_gate.current_Track = track
                                        track.gates.append(temp_gate)
                                    track.gates.append(held_rectangle)
                                    held_rectangle.current_Track = track
                    if isinstance(held_rectangle, cl.Quantum_Gate): 
                        held_rectangle.current_Track.i_gate_cleaner()
                    holding = False
                    held_rectangle = None
        if holding :
            if held_rectangle in level.tracks:
                held_rectangle.rectangle.centery = my
            else :held_rectangle.rectangle.center = (mx, my)

# runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_menu()
