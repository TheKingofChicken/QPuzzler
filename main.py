import pygame as pg
import ctypes
import Views
import Load_Levels
import Circuit_Logic as cl
import Levels
import math
import pickle

renderer = Views.renderer()
levelops = Load_Levels.levelloader()

# main menu buttons
level_Select_Button = pg.Rect(0, 0, 400, 100)
level_Select_Button.center = (renderer.disp_Width/2, 3*renderer.disp_Height/6)
options_Button = pg.Rect(0, 0, 400, 100)
options_Button.center = (renderer.disp_Width/2, 4*renderer.disp_Height/6)
exit_Button = pg.Rect(0, 0, 400, 100)
exit_Button.center = (renderer.disp_Width/2, 5*renderer.disp_Height/6)
main_Menu_Buttons = (level_Select_Button, options_Button, exit_Button)

# options buttons
back_Button = pg.Rect(0, 0, 200, 100)
back_Button.center = (renderer.disp_Width/5, 7*renderer.disp_Height/8)
apply_Button = pg.Rect(0, 0, 200, 100)
apply_Button.center = (4*renderer.disp_Width/5, 7* renderer.disp_Height/8)
help_Button = pg.Rect(0, 0, 400, 100)
help_Button.center =(renderer.disp_Width/2, renderer.disp_Height/2)
option_Buttons = (back_Button, apply_Button, help_Button)

# help screen buttons
back_help_Button = pg.Rect(0, 0, 400, 100)
back_help_Button.center = (210, renderer.disp_Height-60)
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
# includes back_button
start_Button = pg.Rect(0, 0, 200, 100)
start_Button.center = (4*renderer.disp_Width/5, 7* renderer.disp_Height/8)
level_Select_Buttons = (back_Button, start_Button)

level_starters = []
i = 0
for level in Levels:
    Button = pg.Rect(0, 0, 200, 200)
    Button.center = ((i*240) + renderer.disp_Width/5, renderer.disp_Height/4)
    level_starters.append(Button)
    i += 1

# level buttons / setup:
Levels = levelops.load_levels()



# Game loops:
"""each different game "screen", so the main menu, the options page, level select, and the such, has it's own game loop, which contains the 
update and render sections, the player can move between those different game states by using buttons, which just launches the corresponding 
game loop and interrupts the current one"""

# main menu loop
def main_menu():
    click = False #suddenly, python doesn't like it when click's value is given elsewhere, 
    running = True
    while running:
        renderer.main_menu_view(main_Menu_Buttons)

        #the interactive bits, events and what to when they occur, (update section)
        #the bit that checks if the mouse touches a button when it's clicked
        if click:
            if level_Select_Button.collidepoint(mx, my):
                level_select()
            if options_Button.collidepoint(mx, my):
                options_menu()
            if exit_Button.collidepoint(mx, my):
                levelops.save_levels(Levels)
                running = False
        #the bit that takes care of the different events
        click = False
        for event in pg.event.get():
            if event.type is pg.QUIT:
                levelops.save_levels(Levels)
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    levelops.save_levels(Levels)
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (mx, my) = pg.mouse.get_pos()
                    click = True #this one here is the important one
    pg.quit()

def level_select():
    
    click = False
    running = True
    chosen_level = None
    chosen_level_index = 0

    while running:
        renderer.level_select_view(Levels, level_Select_Buttons, chosen_level, level_starters)

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx, my)):
                running = False
            elif start_Button.collidepoint((mx, my)):
                #current_level = pickle.load(open("Levels\level1_file", "rb"))
                level(Levels[chosen_level_index])
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


def options_menu():

    def apply_settings():
            pass
    
    click = False
    running = True
    
    while running :
        renderer.options_menu_view(option_Buttons)

        #update section
        #buttons
        if click:
            if back_Button.collidepoint((mx, my)):
                running = False
            if apply_Button.collidepoint((mx, my)):
                apply_settings()
                running = False
            if help_Button.collidepoint((mx, my)):
                help_screen()
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

def help_screen():

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
        renderer.help_screen_view(help_Buttons)

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

def level(level):
    running = True
    #eveyrthing after this is given a value during the update section, its just given one at the start here so the first render section stop whyning
    holding = False
    held_gate = None
    base_Gate_Rectangle_Y = 890
    base_Gate_Rectangle_X = 30
    track_Rectangle_Y = 70
    track_Rectangle_X = 420
    (mx, my) = (0, 0)
    holding_aux_rectangle = False
    changing_distance = False
    extra_track_button = pg.Rect(430, 10, 80, 50)
    
    #game loop
    while running:
        renderer.level_view(level, held_gate)
        
        for track in level.tracks:
            if track.rectangle.collidepoint((mx, my)) and isinstance(held_gate, cl.Quantum_Gate) and not holding_aux_rectangle:
                new_pos = math.trunc((mx-505)/125)
                if (not new_pos == held_gate.current_Position or not held_gate.current_Track == track) and not changing_distance:
                    held_gate = track.move_gate(new_pos, held_gate)
            for gate in track.gates:
                if isinstance(gate, cl.Conditional_Gate):
                    if gate.conditional:
                        gate.aux_rectangle = gate.conditional.rectangle.inflate(30,30)
                    elif not holding_aux_rectangle:
                        gate.aux_rectangle = pg.Rect(gate.rectangle.midbottom[0] - 15, gate.rectangle.midbottom[1] + 20, 30, 30)
                if gate is held_gate:#skips the whole positioning code if the gate is the one being currently held
                    continue
                gate.rectangle.center = (track.rectangle.x + (125*(1+track.gates.index(gate))), track.rectangle.centery)
            if isinstance(held_gate, cl.Track):#everything inside this if is to change the position of the track when it is dropped
                if track.rectangle.inflate((20, 0)).collidepoint((mx, my)):
                    if level.tracks.index(held_gate) < level.tracks.index(track):
                        offset = 1
                    else: offset = 0
                    level.move_track(level.tracks.index(track)+offset,held_gate)
            # display the track and the total cost the of track
            track.rectangle.y = track_Rectangle_Y + (160 * level.tracks.index(track))
            track.rectangle.x = track_Rectangle_X
            if track is held_gate:
                track.rectangle.centery = my
        #here the code is pretty much exactly repeted, except that it positions the gates on the track, and makes the gates follow the track
        # Box at the bottom of the screen, base_Gates, ...
        for gate in level.available_gates:
            if gate is held_gate:
                continue
            gate.rectangle.x = base_Gate_Rectangle_X + (125 * level.available_gates.index(gate))
            gate.rectangle.y = base_Gate_Rectangle_Y
        
        #update section
        (mx, my) = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type is pg.QUIT:
                levelops.save_levels(Levels)
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    levelops.save_levels(Levels)
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if extra_track_button.collidepoint((mx, my)):
                        level.tracks.append(cl.Track(cl.Quantum_Bit(), level, len(level.tracks)))
                    else:
                        rectangle_is_gate = False
                        for track in level.tracks:
                            for gate in track.gates:
                                if isinstance(gate, cl.I_Gate):
                                    continue
                                elif gate.rectangle.collidepoint(mx, my):
                                    holding = True
                                    held_gate = gate
                                    rectangle_is_gate = True
                                    gate.unlink()
                                elif isinstance(gate, cl.Conditional_Gate):
                                    if gate.aux_rectangle.collidepoint(mx, my):
                                        holding = True
                                        held_gate = gate
                                        rectangle_is_gate = True
                                        holding_aux_rectangle  = True
                                        gate.unlink()
                                        break
                            if rectangle_is_gate:
                                break
                        for gate in level.available_gates:
                            if gate.rectangle.collidepoint(mx, my):
                                holding = True
                                held_gate = gate
                                break
                elif event.button == 2:
                    for track in level.tracks:
                        for gate in track.gates:
                            if (isinstance(gate, cl.AUX_Gate) or isinstance(gate, cl.SWAP_Gate)) and gate.rectangle.collidepoint(mx, my):
                                changing_distance = True
                                held_gate = gate
                                holding = True
                                gate.unlink()
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
                        if track.rectangle.collidepoint(mx, my):
                            track.delete_track()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if holding_aux_rectangle:
                        for track in level.tracks:
                            for gate in track.gates:
                                if gate.rectangle.collidepoint(mx, my) and not isinstance(gate, cl.Conditional_Gate):
                                    level.assign_Conditional(gate, held_gate)
                    elif held_gate in level.available_gates: 
                        new_pos = math.trunc((mx-505)/125)
                    holding = False
                    held_gate = None
                    holding_aux_rectangle = False
                elif event.button == 2:
                    if isinstance(held_gate, cl.SWAP_Gate) or isinstance(held_gate, cl.AUX_Gate):
                        for track in level.tracks:
                            if track.rectangle.collidepoint(mx,my):
                                held_gate.distance = abs(track.position - held_gate.aux_gate.current_Track.position)
                                track.move_gate(held_gate.current_Position, held_gate)
                                break
                        holding = False
                        held_gate = None
                        changing_distance = False        
        if holding :
            if holding_aux_rectangle:
                held_gate.aux_rectangle.center = (mx, my)
            elif changing_distance:
                held_gate.rectangle.centery = my
            elif isinstance(held_gate, cl.SWAP_Gate):
                held_gate.rectangle.center = (mx,my)
                held_gate.aux_gate.rectangle.center = (mx, my+(held_gate.aux_gate.distance * 150))
            elif isinstance(held_gate, cl.AUX_Gate):
                held_gate.rectangle.center = (mx,my)
                held_gate.aux_gate.rectangle.center = (mx, my-(held_gate.aux_gate.distance * 150))
            else :held_gate.rectangle.center = (mx, my)


# runs main_Menu() if the file's name is main, which it is, just as a safekeeping measure
if __name__ == "__main__":
    main_menu()