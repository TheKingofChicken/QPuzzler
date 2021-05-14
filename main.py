import pygame as pg
import ctypes
import Circuit_Logic as cl
import Levels
import math
import pickle

# without this line, pygame thinks the screen is only 1536 pixels wide, which fucks up elements whose position depends on the resolution
ctypes.windll.user32.SetProcessDPIAware()

# Initialise pygame
pg.init()

# setting up display
display = pg.display.set_mode((1920, 1080))
pg.display.set_caption('QPuzzler')
disp_Width = display.get_width()
disp_Height = display.get_height()
fps_Limiter = pg.time.Clock()

# text shenanigans
pg.font.init()
normal_Font = pg.font.Font("square.ttf", 48)
menu_Font = pg.font.Font("square.ttf", 192)
small_font = pg.font.Font("square.ttf", 24)
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
    "light grey" : (200,200,200), 
    "blue" : (0, 137, 255), 
    "red" : (255, 50, 50), 
    "yellow" : (240, 240, 50),
    "purple" : (138,43,226),
    "pink" : (255,105,180),
    "dark green" : (50,205,50)
    }

# Things to draw the gates
gatedict = {
    "H" : colordict["blue"],
    "X" : colordict["red"],
    "T" : colordict["yellow"],
    "Z" : colordict["purple"],
    "S" : colordict["pink"],
    "if" : colordict["black"],
    "SWAP" : colordict["dark green"]
}

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
help_Button = pg.Rect(0, 0, 400, 100)
help_Button.center =(disp_Width/2, disp_Height/2)
option_Buttons = (back_Button, apply_Button, help_Button)

# help screen buttons
back_help_Button = pg.Rect(0, 0, 400, 100)
back_help_Button.center = (210, disp_Height-60)
qubit_help_Button = pg.Rect(0, 0, 400, 100)
qubit_help_Button.center = (210, 60)
swapgate_help_Button = pg.Rect(0, 0, 400, 100)
swapgate_help_Button.center = (210, 180)
hgate_help_Button = pg.Rect(0, 0, 400, 100)
hgate_help_Button.center = (210, 300)
xgate_help_Button = pg.Rect(0, 0, 400, 100)
xgate_help_Button.center = (210, 420)
tgate_help_Button = pg.Rect(0, 0, 400, 100)
tgate_help_Button.center = (210, 540)
zgate_help_Button = pg.Rect(0, 0, 400, 100)
zgate_help_Button.center = (210, 660)
sgate_help_Button = pg.Rect(0, 0, 400, 100)
sgate_help_Button.center = (210, 780)
help_Buttons = (back_help_Button, qubit_help_Button, swapgate_help_Button, hgate_help_Button, xgate_help_Button, tgate_help_Button, zgate_help_Button, sgate_help_Button)



# level select buttons
base_Gates = [cl.H_Gate(80, None, None, None, rectangle = pg.Rect(0, 0, 100, 100)), cl.X_Gate(100, None, None, None, rectangle = pg.Rect(0, 0, 100, 100)), cl.T_Gate(120,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.Z_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.S_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.Conditional_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.SWAP_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100))]
current_level = cl.Level([], [], base_Gates,"goal and tutorial bit", "test level")
#pickled_level = pickle.dump(current_level, open("Levels\leveltest_file", "wb"))
Levels = [current_level]
level1 = pickle.load(open("Levels\level1_file", "rb"))
Levels.append(level1)
level2 = pickle.load(open("Levels\level2_file", "rb"))
Levels.append(level2)
level3 = pickle.load(open("Levels\level3_file", "rb"))
Levels.append(level3)
level4 = pickle.load(open("Levels\level4_file", "rb"))
Levels.append(level4)
# includes back_button
start_Button = pg.Rect(0, 0, 200, 100)
start_Button.center = (4*disp_Width/5, 7* disp_Height/8)
level_Select_Buttons = (back_Button, start_Button)
level_starters = []
i = 0
for level in Levels:
    Button = pg.Rect(0, 0, 200, 200)
    Button.center = ((i*240) + disp_Width/5, disp_Height/4)
    level_starters.append(Button)
    i += 1

# level buttons / setup:

"""
# level 1
level1_ogfile = cl.Level([], [], base_Gates, "goal : tbd", "level 1")
#level1_ogfile.add_track(cl.Track(0))
#level1_ogfile.add_track(cl.Track(0))
#level1_ogfile.goal_text = "goal : tbd"
#level1_ogfile.name = "level 1"
pickled_level1 = pickle.dump(level1_ogfile, open("Levels\level1_file", "wb"))

# level 2
#gate1_level2 = cl.H_Gate(80, 0, 0, 0)
#gate2_level2 = cl.X_Gate(100, 0, 0, 0)
#gate3_level2 = cl.T_Gate(120, 0, 0, 0)
#track1_level2 = cl.Track(0)
#track2_level2 = cl.Track(0)
#track3_level2 = cl.Track(0)

level2_ogfile = cl.Level([], [], base_Gates, "goal : tbd", "level 2")
#track1_level2.gates.append(gate1_level2)
#gate1_level2.current_Track = track1_level2
#track2_level2.gates.append(gate2_level2)
#gate2_level2.current_Track = track2_level2
#track3_level2.gates.append(gate3_level2)
#gate3_level2.current_Track = track3_level2
#level2_ogfile.add_track(track1_level2)
#level2_ogfile.add_track(track2_level2)
#level2_ogfile.add_track(track3_level2)
#level2_ogfile.goal_text = "goal : tbd"
#level2_ogfile.name = "level 2"
pickled_level2 = pickle.dump(level2_ogfile, open("Levels\level2_file", "wb"))
#print (f"pickled level 2 file: \n{pickled_level2}\n")

# level 3
#gate1_level3 = cl.H_Gate(80, 0, 0, 0)
#gate2_level3 = cl.X_Gate(100, 0, 0, 0)
#gate3_level3 = cl.T_Gate(120, 0, 0, 0)
#track1_level3 = cl.Track(0)
#track2_level3 = cl.Track(0)
#track3_level3 = cl.Track(0)

level3_ogfile = cl.Level([], [], base_Gates, "goal : tbd", "level 3")
#track1_level3.gates.append(gate1_level3)
#gate1_level3.current_Track = track1_level3
#track1_level3.gates.append(gate2_level3)
#gate2_level3.current_Track = track1_level3
#track2_level3.gates.append(gate3_level3)
#gate3_level3.current_Track = track2_level3
#level3_ogfile.add_track(track1_level3)
#level3_ogfile.add_track(track2_level3)
#level3_ogfile.add_track(track3_level3)
#level3_ogfile.goal_text = "goal : tbd"
#level3_ogfile.name = "level 3"
pickled_level3 = pickle.dump(level3_ogfile, open("Levels\level3_file", "wb"))
#print (f"pickled level 3 file: \n{pickled_level3}\n")

# level 4
#gate1_level4 = cl.H_Gate(80, 0, 0, 0)
#gate2_level4 = cl.X_Gate(100, 0, 0, 0)
#gate3_level4 = cl.T_Gate(120, 0, 0, 0)
#track1_level4 = cl.Track(0)
#track2_level4 = cl.Track(0)
#track3_level4 = cl.Track(0)

level4_ogfile = cl.Level([], [], base_Gates, "goal : tbd", "level 4")
#track1_level4.gates.append(gate1_level4)
#gate1_level4.current_Track = track1_level4
#track1_level4.gates.append(gate2_level4)
#gate2_level4.current_Track = track1_level4
#track2_level4.gates.append(gate3_level4)
#gate3_level4.current_Track = track2_level4
#level4_ogfile.add_track(track1_level4)
#level4_ogfile.add_track(track2_level4)
#level4_ogfile.add_track(track3_level4)
#level4_ogfile.goal_text = "goal : tbd"
#level4_ogfile.name = "level 4"
pickled_level4 = pickle.dump(level4_ogfile, open("Levels\level4_file", "wb"))
#print (f"pickled level 4 file: \n{pickled_level4}\n")
"""

def save_levels(levels):
    levelfile_text = ["Levels\leveltest_file", "Levels\level1_file", "Levels\level2_file", "Levels\level3_file", "Levels\level4_file"]
    for x in range(len(levels)):
        pickled_level = pickle.dump(levels[x], open(levelfile_text[x], "wb"))

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
                save_levels(Levels)
                running = False
        #the bit that takes care of the different events
        click = False
        for event in pg.event.get():
            if event.type is pg.QUIT:
                save_levels(Levels)
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    save_levels(Levels)
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pg.mouse.get_pos()
                    click = True #this one here is the important one
    pg.quit()

def level_select(display):
    
    click = False
    running = True
    chosen_level = None
    chosen_level_index = 0

    while running:
        fps_Limiter.tick(60)
        #render section
        display.fill(colordict["white"])
        for button in level_Select_Buttons:
            pg.draw.rect(display, colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        for button in level_starters:
            if button is chosen_level:
                pg.draw.rect(display, colordict["red"], button, 10)
            else: pg.draw.rect(display, colordict["black"], button, 10)
        draw_text(display, "BACK", colordict["black"], fontdict["normal"], disp_Width/5, 7*disp_Height/8)
        draw_text(display, "START", colordict["black"], fontdict["normal"], 4*disp_Width/5, 7* disp_Height/8)
        for x in range(len(Levels)):
            if level_starters[x] is chosen_level:
                draw_text(display, Levels[x].name, colordict["red"], fontdict["normal"], disp_Width/5 + 240*x, disp_Height/4)
            else: draw_text(display, Levels[x].name, colordict["black"], fontdict["normal"], disp_Width/5 + 240*x, disp_Height/4)
        pg.display.update()

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx, my)):
                running = False
            elif start_Button.collidepoint((mx, my)):
                #current_level = pickle.load(open("Levels\level1_file", "rb"))
                level(display, Levels[chosen_level_index])
                chosen_level = None
            for button in level_starters:
                if button.collidepoint((mx, my)):
                    if chosen_level is button:
                        chosen_level = None
                    else:
                        chosen_level = button
                        chosen_level_index = level_starters.index(button)
                    
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
        draw_text(display, "HELP", colordict["black"], fontdict["normal"], disp_Width/2, disp_Height/2)
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
            if help_Button.collidepoint((mx, my)):
                help_screen(display)
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

def help_screen(display):

    running = True
    click = False
    chosen_button_text = ""

    qubit_help_text = "1"
    swapgate_help_text = "2"
    hgate_help_text = "3"
    xgate_help_text = "4"
    tgate_help_text = "5"
    zgate_help_text = "6"
    sgate_help_text = "7"

    while running :
        fps_Limiter.tick(60)

        #render section
        display.fill(colordict["white"])
        for button in help_Buttons:
            pg.draw.rect(display, colordict["black"], button, 10)
        draw_text(display, chosen_button_text, colordict["black"], fontdict["normal"], disp_Width/2, disp_Height/2)
        draw_text(display, "BACK", colordict["black"], fontdict["normal"], 210, disp_Height-60)
        draw_text(display, "QUANTUM BIT", colordict["black"], fontdict["normal"], 210, 60)
        draw_text(display, "SWAP GATE", colordict["black"], fontdict["normal"], 210, 180)
        draw_text(display, "H GATE", colordict["black"], fontdict["normal"], 210, 300)
        draw_text(display, "X GATE", colordict["black"], fontdict["normal"], 210, 420)
        draw_text(display, "T GATE", colordict["black"], fontdict["normal"], 210, 540)
        draw_text(display, "Z GATE", colordict["black"], fontdict["normal"], 210, 660)
        draw_text(display, "S GATE", colordict["black"], fontdict["normal"], 210, 780)
        pg.display.update()

        #update section
        #buttons
        if click:
            if back_help_Button.collidepoint((mx, my)):
                running = False
            elif qubit_help_Button.collidepoint((mx, my)):
                chosen_button_text = qubit_help_text
            elif swapgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = swapgate_help_text
            elif hgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = hgate_help_text
            elif xgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = xgate_help_text
            elif tgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = tgate_help_text
            elif zgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = zgate_help_text
            elif sgate_help_Button.collidepoint((mx, my)):
                chosen_button_text = sgate_help_text

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
    base_Gate_Rectangle_Y = 890
    base_Gate_Rectangle_X = 30
    track_Rectangle_Y = 70
    track_Rectangle_X = 420
    (mx, my) = (0, 0)
    holding_aux_rectangle = False
    holding_aux_gate = False
    extra_track_button = pg.Rect(430, 10, 80, 50)
    
    def draw_gate(gate):
        if isinstance(gate, cl.I_Gate):
            pass
        elif isinstance(gate,cl.Conditional_Gate):
            pg.draw.rect(display, colordict["grey"], gate.rectangle, 10)
            draw_text(display, str(gate), colordict["grey"], fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
            if gate.current_Track:
                pg.draw.rect(display, colordict["grey"], gate.aux_rectangle, 10)
                if gate.rectangle.y < gate.aux_rectangle.y:
                    pg.draw.line(display,colordict["grey"], gate.rectangle.midbottom, gate.aux_rectangle.midtop, 10)
                else:
                    pg.draw.line(display,colordict["grey"], gate.rectangle.midtop, gate.aux_rectangle.midbottom, 10)
        elif isinstance(gate, cl.SWAP_Gate):
            pg.draw.rect(display, gatedict[str(gate)], gate.rectangle)
            pg.draw.rect(display, colordict["black"], gate.rectangle, 10)
            draw_text(display, str(gate), colordict["black"], fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
            
            if not gate in level.available_gates and not gate.current_Track:
                pg.draw.rect(display, gatedict[str(gate)], gate.aux_gate.rectangle)
                pg.draw.rect(display, colordict["black"], gate.aux_gate.rectangle, 10)
                draw_text(display, str(gate), colordict["black"], fontdict["normal"], gate.aux_gate.rectangle.centerx, gate.aux_gate.rectangle.centery)
        else:
            pg.draw.rect(display, gatedict[str(gate)], gate.rectangle)
            pg.draw.rect(display, colordict["black"], gate.rectangle, 10)
            draw_text(display, str(gate), colordict["black"], fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
    
    def draw_level(level):
    
        first_layer_elements = []
    
        display.fill(colordict["white"])
    
        pg.draw.rect(display, colordict["white"], pg.Rect(10, 10, 400, disp_Height-240))
        pg.draw.rect(display, colordict["black"], pg.Rect(10, 10, 400, disp_Height-240), 10)
    
        pg.draw.rect(display, colordict["white"], pg.Rect(10, disp_Height-210, disp_Width-20, 200))
        pg.draw.rect(display, colordict["black"], pg.Rect(10, disp_Height-210, disp_Width-20, 200), 10)
        draw_text(display, level.goal_text, colordict["black"], fontdict["normal"], 200, 35)    
    
        pg.draw.rect(display, colordict["grey"], pg.Rect(430, 10, 80, 50), 10)
        pg.draw.line(display, colordict["grey"],(470, 20),(470,50), 10)
        pg.draw.line(display, colordict["grey"],(455, 35),(485,35), 10)
    
        for track in level.tracks:
            pg.draw.rect(display, colordict["light grey"], track.rectangle, 10)
            for gate in track.gates:
                if isinstance(gate, cl.Conditional_Gate):
                    first_layer_elements.append(gate)
                    continue
                draw_gate(gate)
        for gate in level.available_gates:
            draw_gate(gate)
        for gate in first_layer_elements:
            draw_gate(gate)
    
    #game loop
    while running:
        fps_Limiter.tick(60)
        
        draw_level(level)
        pg.display.update()
        
        for track in level.tracks:
            if track.rectangle.collidepoint((mx, my)) and isinstance(held_rectangle, cl.Quantum_Gate) and not holding_aux_rectangle:
                new_pos = math.trunc((mx-505)/125)
                if new_pos != held_rectangle.current_Position or held_rectangle.rectangle.collidepoint((mx,my)):
                    held_rectangle = track.move_gate(new_pos, held_rectangle)
                    if isinstance(held_rectangle, cl.SWAP_Gate):
                        try:
                            if holding_aux_gate:
                                level.tracks[level.tracks.index(held_rectangle.current_Track) - 1].move_gate(new_pos, held_rectangle.aux_gate)
                            else:
                                level.tracks[level.tracks.index(held_rectangle.current_Track) + 1].move_gate(new_pos, held_rectangle.aux_gate)
                        except IndexError:
                            pass
            for gate in track.gates:
                if isinstance(gate, cl.Conditional_Gate):
                    if gate.conditional:
                        gate.aux_rectangle = gate.conditional.rectangle.inflate(30,30)
                    elif not holding_aux_rectangle:
                        gate.aux_rectangle = pg.Rect(gate.rectangle.midbottom[0] - 15, gate.rectangle.midbottom[1] + 20, 30, 30)
                if gate is held_rectangle:#skips the whole positioning code if the gate is the one being currently held
                    continue
                gate.rectangle.center = (track.rectangle.x + (125*(1+track.gates.index(gate))), track.rectangle.centery)
            if isinstance(held_rectangle, cl.Track):#everything inside this if is to change the position of the track when it is dropped
                if track.rectangle.inflate((20, 0)).collidepoint((mx, my)):
                    if level.tracks.index(held_rectangle) < level.tracks.index(track):
                        offset = 1
                    else: offset = 0
                    level.move_track(level.tracks.index(track)+offset,held_rectangle)
            # display the track and the total cost the of track
            track.rectangle.y = track_Rectangle_Y + (160 * level.tracks.index(track))
            track.rectangle.x = track_Rectangle_X
            if track is held_rectangle:
                track.rectangle.centery = my
        #here the code is pretty much exactly repeted, except that it positions the gates on the track, and makes the gates follow the track
        # Box at the bottom of the screen, base_Gates, ...
        for gate in level.available_gates:
            if gate is held_rectangle:
                continue
            gate.rectangle.x = base_Gate_Rectangle_X + (125 * level.available_gates.index(gate))
            gate.rectangle.y = base_Gate_Rectangle_Y
        
        #update section
        (mx, my) = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type is pg.QUIT:
                save_levels(Levels)
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    save_levels(Levels)
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if extra_track_button.collidepoint((mx, my)):
                        level.tracks.append(cl.Track(cl.Quantum_Bit, level, len(level.tracks)))
                    else:
                        rectangle_is_gate = False
                        for track in level.tracks:
                            for gate in track.gates:
                                if isinstance(gate, cl.I_Gate):
                                    continue
                                elif isinstance(gate, cl.SWAP_Gate):
                                    if gate.aux_gate.rectangle.collidepoint(mx, my):
                                        holding = True
                                        rectangle_is_gate = True
                                        held_rectangle = gate
                                        gate.unlink()
                                        if level.tracks.index(gate.current_Track) > level.tracks.index(gate.aux_gate.current_Track):
                                            holding_aux_gate = False
                                        else:
                                            holding_aux_gate = True
                                elif gate.rectangle.collidepoint(mx, my):
                                    holding = True
                                    held_rectangle = gate
                                    rectangle_is_gate = True
                                    gate.unlink()
                                elif isinstance(gate, cl.Conditional_Gate):
                                    if gate.aux_rectangle.collidepoint(mx, my):
                                        holding = True
                                        held_rectangle = gate
                                        rectangle_is_gate = True
                                        holding_aux_rectangle  = True
                                        gate.unlink()
                                        break
                            if rectangle_is_gate:
                                break
                            if track.rectangle.collidepoint(mx, my):
                                holding = True
                                held_rectangle = track
                                break
                        for gate in level.available_gates:
                            if gate.rectangle.collidepoint(mx, my):
                                holding = True
                                held_rectangle = gate
                                break
                elif event.button == 3:
                    gate_is_found = False
                    for track in level.tracks:
                        for gate in track.gates:
                            if isinstance(gate, cl.Conditional_Gate) and gate.aux_rectangle.collidepoint(mx, my):
                                gate.unlink()
                                gate_is_found = True
                                break
                            if gate.rectangle.collidepoint(mx, my):
                                track.delete_gate(gate)
                                gate_is_found = True
                                break
                        if gate_is_found:
                            break
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if holding_aux_rectangle:
                        for track in level.tracks:
                            for gate in track.gates:
                                if gate.rectangle.collidepoint(mx, my) and not isinstance(gate, cl.Conditional_Gate):
                                    level.assign_Conditional(gate, held_rectangle)
                    elif held_rectangle in level.available_gates: 
                        new_pos = math.trunc((mx-505)/125)
                        for track in level.tracks:
                            if track.rectangle.collidepoint((mx, my)):
                                track.move_gate(new_pos, held_rectangle)
                            if isinstance(held_rectangle, cl.SWAP_Gate):
                                try:
                                    if holding_aux_gate:
                                        level.tracks[level.tracks.index(held_rectangle.current_Track) - 1].move_gate(new_pos, held_rectangle.aux_gate)
                                    else:
                                        level.tracks[level.tracks.index(held_rectangle.current_Track) + 1].move_gate(new_pos, held_rectangle.aux_gate)
                                except IndexError:
                                    pass
                    holding = False
                    held_rectangle = None
                    holding_aux_rectangle = False
                    holding_aux_gate = False
        if holding :
            if held_rectangle in level.tracks:
                held_rectangle.rectangle.centery = my
            elif holding_aux_rectangle:
                held_rectangle.aux_rectangle.center = (mx, my)
            elif isinstance(held_rectangle, cl.SWAP_Gate):
                if holding_aux_gate:
                    held_rectangle.rectangle.center = (mx,my)
                    held_rectangle.aux_gate.rectangle.center = (mx, my-120)
                else:
                    held_rectangle.rectangle.center = (mx,my)
                    held_rectangle.aux_gate.rectangle.center = (mx, my+120)
            else :held_rectangle.rectangle.center = (mx, my)


# runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_menu()