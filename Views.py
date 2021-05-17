import pygame as pg
import Circuit_Logic as cl
import ctypes
import numpy
import math
from numpy import array
import itertools

class renderer():
    
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
    
    gatedict = {
        "H" : colordict["blue"],
        "X" : colordict["red"],
        "T" : colordict["yellow"],
        "Z" : colordict["purple"],
        "S" : colordict["pink"],
        "if" : colordict["black"],
        "SWAP" : colordict["dark green"]
        }
        
    def __init__(self):

        ctypes.windll.user32.SetProcessDPIAware()

        # Initialise pygame
        pg.init()
        
        # setting up display
        self.display = pg.display.set_mode((1920, 1080))
        pg.display.set_caption('QPuzzler')
        self.disp_Width = self.display.get_width()
        self.disp_Height = self.display.get_height()
        self.fps_Limiter = pg.time.Clock()

        # text shenanigans
        pg.font.init()

        # colors we're actually gonna use
        self.colordict = {
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
        self.gatedict = {
            "H" : self.colordict["blue"],
            "X" : self.colordict["red"],
            "T" : self.colordict["yellow"],
            "Z" : self.colordict["purple"],
            "S" : self.colordict["pink"],
            "if" : self.colordict["black"],
            "SWAP" : self.colordict["dark green"]
        }
        # text shenanigans
        normal_Font = pg.font.Font("square.ttf", 48)
        menu_Font = pg.font.Font("square.ttf", 192)
        self.fontdict = {
            "menu" : menu_Font, 
            "normal" : normal_Font
        }


    def draw_text(self, display, text, color, font, X, Y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (X, Y)
        display.blit(textobj, textrect)
    
    def draw_quantum_state(self, state, x, y, vertically = True, background = colordict["white"]): #used to represent on screen the state of a qbit
        new_surface = pg.Surface((42*(len(state)+1),60))
        new_surface.fill(background)
        pg.draw.line(new_surface,self.colordict["black"], (5,5), (5,55), 2)
        pg.draw.line(new_surface,self.colordict["black"], (42*(len(state)+1)-5,5), (42*(len(state)+1)-5,55), 2)
        pg.draw.line(new_surface,self.colordict["black"], (5,5), (32,5), 2)
        pg.draw.line(new_surface,self.colordict["black"], (5,55), (32,55), 2)
        pg.draw.line(new_surface,self.colordict["black"], (42*(len(state)+1)-5,5), (42*(len(state)+1)-30,5), 2)
        pg.draw.line(new_surface,self.colordict["black"], (42*(len(state)+1)-5,55), (42*(len(state)+1)-30,55), 2)
        if vertically:
            new_surface = pg.transform.rotate(new_surface,-90)
        for state_index in range(len(state)):
            arrow_vector = (math.copysign(numpy.real(state[state_index])**2, numpy.real(state[state_index])), math.copysign(numpy.imag(state[state_index])**2, numpy.imag(state[state_index])))
            if vertically:
                arrow = ((30 + 20*arrow_vector[0], 42*(state_index+1) - 20*arrow_vector[1]),(30 - 20*arrow_vector[0], 42*(state_index+1) + 20*arrow_vector[1]))
            else:
                arrow = ((42*(state_index+1) + 20*arrow_vector[0], 30 - 20*arrow_vector[1]),(42*(state_index+1) - 20*arrow_vector[0], 30 + 20*arrow_vector[1]))
            pg.draw.line(new_surface,self.colordict["black"],arrow[0], arrow[1], 3)
            pg.draw.circle(new_surface,self.colordict["black"], arrow[0], 5)
        rect = new_surface.get_rect()
        rect.center = (x,y)
        self.display.blit(new_surface, rect)
        
    def draw_gate(self, level, gate, held_rectangle):
        if isinstance(gate, cl.I_Gate):
            pass
        elif isinstance(gate,cl.Conditional_Gate):
            pg.draw.rect(self.display, self.colordict["grey"], gate.rectangle, 10)
            self.draw_text(self.display, str(gate), self.colordict["grey"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
            if gate.current_Track or gate is held_rectangle:
                pg.draw.rect(self.display, self.colordict["grey"], gate.aux_rectangle, 10)
                if gate.rectangle.y < gate.aux_rectangle.y:
                    pg.draw.line(self.display,self.colordict["grey"], gate.rectangle.midbottom, gate.aux_rectangle.midtop, 10)
                else:
                    pg.draw.line(self.display,self.colordict["grey"], gate.rectangle.midtop, gate.aux_rectangle.midbottom, 10)
        elif isinstance(gate, cl.SWAP_Gate):
            pg.draw.rect(self.display, self.gatedict[str(gate)], gate.rectangle)
            pg.draw.rect(self.display, self.colordict["black"], gate.rectangle, 10)
            self.draw_text(self.display, str(gate), self.colordict["black"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
            
            if gate is held_rectangle or not gate in level.available_gates:
                pg.draw.line(self.display, self.colordict["black"], gate.rectangle.midbottom, gate.aux_gate.rectangle.midtop, 10)
            
            if gate is held_rectangle:
                pg.draw.rect(self.display, self.gatedict[str(gate)], gate.aux_gate.rectangle)
                pg.draw.rect(self.display, self.colordict["black"], gate.aux_gate.rectangle, 10)
                self.draw_text(self.display, str(gate), self.colordict["black"], self.fontdict["normal"], gate.aux_gate.rectangle.centerx, gate.aux_gate.rectangle.centery)
        else:
            pg.draw.rect(self.display, self.gatedict[str(gate)], gate.rectangle)
            pg.draw.rect(self.display, self.colordict["black"], gate.rectangle, 10)
            self.draw_text(self.display, str(gate), self.colordict["black"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)

        if gate in level.available_gates and not gate is held_rectangle:
            self.draw_text(self.display, str(gate.cost), self.colordict["black"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery + 100)
    
    def main_menu_view(self, main_Menu_Buttons):
        self.fps_Limiter.tick(60)
        #everything that needs to be rendered:
        self.display.fill(self.colordict["white"])
        for button in main_Menu_Buttons:
            pg.draw.rect(self.display, self.colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        self.draw_text(self.display, "QPUZZLER", self.colordict["black"], self.fontdict["menu"], self.disp_Width/2, self.disp_Height/5)
        self.draw_text(self.display, "level SELECT", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, 3*self.disp_Height/6)
        self.draw_text(self.display, "OPTIONS", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, 4*self.disp_Height/6)
        self.draw_text(self.display, "EXIT", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, 5*self.disp_Height/6)
        pg.display.update()
    
    def level_select_view(self, levels, level_Select_Buttons, chosen_level, level_starters):
        self.fps_Limiter.tick(60)
        #render section
        self.display.fill(self.colordict["white"])
        for button in level_Select_Buttons:
            pg.draw.rect(self.display, self.colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        for button in level_starters:
            if button is chosen_level:
                pg.draw.rect(self.display, self.colordict["red"], button, 10)
            else: pg.draw.rect(self.display, self.colordict["black"], button, 10)
        self.draw_text(self.display, "BACK", self.colordict["black"], self.fontdict["normal"], self.disp_Width/5, 7*self.disp_Height/8)
        self.draw_text(self.display, "START", self.colordict["black"], self.fontdict["normal"], 4*self.disp_Width/5, 7* self.disp_Height/8)
        i = 0
        j = 0
        for x in range(len(levels)):
            if level_starters[x] is chosen_level:
                self.draw_text(self.display, levels[x].name, self.colordict["red"], self.fontdict["normal"], self.disp_Width/5 + (240*i), self.disp_Height/4 + (240*j))
            else: self.draw_text(self.display, levels[x].name, self.colordict["black"], self.fontdict["normal"], self.disp_Width/5 + (240*i), self.disp_Height/4 + (240*j))
            i += 1
            if i > 5:
                i = 0
                j += 1
        pg.display.update()
    
    def options_menu_view(self, option_Buttons):
        self.fps_Limiter.tick(60)
        #render section
        self.display.fill(self.colordict["white"])
        for button in option_Buttons:
            pg.draw.rect(self.display, self.colordict["black"], button, 10) #the 4th parametter replaces the filled rectangle with an the outline of a rectangle
        self.draw_text(self.display, "OPTIONS", self.colordict["black"], self.fontdict["menu"], self.disp_Width/2, self.disp_Height/5)
        self.draw_text(self.display, "HELP", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, self.disp_Height/2)
        self.draw_text(self.display, "BACK", self.colordict["black"], self.fontdict["normal"], self.disp_Width/5, 7*self.disp_Height/8)
        self.draw_text(self.display, "APPLY", self.colordict["black"], self.fontdict["normal"], 4*self.disp_Width/5, 7*self.disp_Height/8)
        pg.display.update()
    
    def help_screen_view(self, help_Buttons, chosen_button_text):
        self.fps_Limiter.tick(60)

        #render section
        self.display.fill(self.colordict["white"])
        for button in help_Buttons:
            pg.draw.rect(self.display, self.colordict["black"], button, 10)
        self.draw_text(self.display, "", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, self.disp_Height/2)
        self.draw_text(self.display, "BACK", self.colordict["black"], self.fontdict["normal"], 210, self.disp_Height-60)
        self.draw_text(self.display, "QUANTUM BIT", self.colordict["black"], self.fontdict["normal"], 210, 60)
        self.draw_text(self.display, "SWAP GATE", self.colordict["black"], self.fontdict["normal"], 210, 180)
        self.draw_text(self.display, "H GATE", self.colordict["black"], self.fontdict["normal"], 210, 300)
        self.draw_text(self.display, "X GATE", self.colordict["black"], self.fontdict["normal"], 210, 420)
        self.draw_text(self.display, "T GATE", self.colordict["black"], self.fontdict["normal"], 210, 540)
        self.draw_text(self.display, "Z GATE", self.colordict["black"], self.fontdict["normal"], 210, 660)
        self.draw_text(self.display, "S GATE", self.colordict["black"], self.fontdict["normal"], 210, 780)
        self.draw_text(self.display, "if GATE", self.colordict["black"], self.fontdict["normal"], 210, 900)
        i = 0
        for x in range(len(chosen_button_text)):
            self.draw_text(self.display, chosen_button_text[x], self.colordict["black"], self.fontdict["normal"], self.disp_Width/2 + 200, 200 + (100*i))
            i += 1
        pg.display.update()
    
    def level_view(self, level, held_rectangle):
        
        self.fps_Limiter.tick(60)
        
        first_layer_elements = []
    
        self.display.fill(self.colordict["white"])
    
        pg.draw.rect(self.display, self.colordict["white"], pg.Rect(10, 10, 400, self.disp_Height-240))
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(10, 10, 400, self.disp_Height-240), 10)
        self.draw_text(self.display, level.name, self.colordict["black"], self.fontdict["normal"], 210, 60)
        
        for track in level.tracks:
            self.draw_quantum_state(track.input[0].state, 210, track.rectangle.centery)
        
        self.draw_text(self.display, str(level.total_Cost), self.colordict["black"], self.fontdict["normal"], 210, self.disp_Height - 280)
        self.draw_text(self.display, level.goal_text, self.colordict["black"], self.fontdict["normal"], self.disp_Width/2 + 200, self.disp_Height - 280)
        pg.draw.rect(self.display, self.colordict["white"], pg.Rect(10, self.disp_Height-210, self.disp_Width-340, 200))
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(10, self.disp_Height-210, self.disp_Width-340, 200), 10)
    
        pg.draw.rect(self.display, self.colordict["grey"], pg.Rect(430, 10, 80, 50), 10)
        pg.draw.line(self.display, self.colordict["grey"],(470, 20),(470,50), 10)
        pg.draw.line(self.display, self.colordict["grey"],(455, 35),(485,35), 10)
        
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(self.disp_Width - 310, self.disp_Height-100, 300, 90), 10)
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(self.disp_Width - 310, self.disp_Height-210, 300, 90), 10)
        self.draw_text(self.display,"execute", self.colordict["black"], self.fontdict["normal"], self.disp_Width-150, self.disp_Height - 55)
        self.draw_text(self.display,"help", self.colordict["black"], self.fontdict["normal"], self.disp_Width-150, self.disp_Height - 159)
        
        for track in level.tracks:
            pg.draw.rect(self.display, self.colordict["light grey"], track.rectangle, 10)
        for track in level.tracks:
            for gate in track.gates:
                if isinstance(gate, cl.Conditional_Gate):
                    first_layer_elements.append(gate)
                    continue
                self.draw_gate(level, gate, held_rectangle)
        for gate in level.available_gates:
            self.draw_gate(level, gate, held_rectangle)
        for gate in first_layer_elements:
            self.draw_gate(level, gate, held_rectangle)
        pg.display.update()
        
    def level_end_screen_view(self, level, red_squares, test_number):
        
        self.fps_Limiter.tick(60)
        
        background = pg.Rect(self.disp_Width/2, self.disp_Height/2, self.disp_Width/2, self.disp_Height/2)
        background.center = (self.disp_Width/2, self.disp_Height/2)
        pg.draw.rect(self.display, self.colordict["white"], background)
        pg.draw.rect(self.display, self.colordict["black"], background, 10)
        
        self.draw_text(self.display, "input", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + self.disp_Width/8, self.disp_Width/4 + self.disp_Width/7)
        self.draw_text(self.display, "correct answer", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + 2* self.disp_Width/8, self.disp_Width/4 + self.disp_Width/7)
        self.draw_text(self.display, "answer", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + 3* self.disp_Width/8, self.disp_Width/4 + self.disp_Width/7)
        
        level.output = [array([complex(0,1), complex(0,0)])]
        quantum_states = [level.tracks, level.output, level.snapshots]
        for column in range(len(quantum_states)):
            for row in range(len(quantum_states[column])):
                if hasattr(quantum_states[column][row], "input"):
                    if red_squares > 0:
                        self.draw_quantum_state(quantum_states[column][row].input[test_number].state, self.disp_Width/4 + (column+1)* self.disp_Width/8, self.disp_Height/4 + (row+1) * self.disp_Height/(2*(1+len(quantum_states[column]))), vertically = False, background= self.colordict["red"])
                        red_squares -=5
                    else:
                        self.draw_quantum_state(quantum_states[column][row].input[test_number].state, self.disp_Width/4 + (column+1)* self.disp_Width/8, self.disp_Height/4 + (row+1) * self.disp_Height/(2*(1+len(quantum_states[column]))), vertically = False)
                else:
                    if red_squares > 0:
                        self.draw_quantum_state(quantum_states[column][test_number], self.disp_Width/4 + (column+1)* self.disp_Width/8, self.disp_Height/4 + (row+1) * self.disp_Height/(2*(1+len(quantum_states[column]))), background = self.colordict["red"])
                        red_squares -= 5
                    else:
                        self.draw_quantum_state(quantum_states[column][test_number], self.disp_Width/4 + (column+1)* self.disp_Width/8, self.disp_Height/4 + (row+1) * self.disp_Height/(2*(1+len(quantum_states[column]))))
        pg.display.update()
        if red_squares > 0:
            return True
    
    def loss_View(self, uncorrect_arrays, back_button):
        background = pg.Rect(self.disp_Width/2, self.disp_Height/2, self.disp_Width/2, self.disp_Height/2)
        background.center = (self.disp_Width/2, self.disp_Height/2)
        pg.draw.rect(self.display, self.colordict["white"], background)
        pg.draw.rect(self.display, self.colordict["black"], background, 10)
        #pg.draw.rect(self.display, self.colordict["black"], back_button, 10)
        
        #self.draw_text(self.display, "back", self.colordict["black"], self.fontdict["normal"], back_button.centerx, back_button.centery)
        self.draw_text(self.display, "error", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, self.disp_Height/2 - self.disp_Height/8)
        self.draw_text(self.display, "input", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + self.disp_Width/8, self.disp_Width/4 + self.disp_Width/7)
        self.draw_text(self.display, "good answer", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + 2* self.disp_Width/8, self.disp_Width/4 + self.disp_Width/7)
        self.draw_text(self.display, "your answer", self.colordict["black"], self.fontdict["normal"],self.disp_Width/4 + 3* self.disp_Width/8 + 15, self.disp_Width/4 + self.disp_Width/7)
        for array_index in range(len(uncorrect_arrays)):
            if isinstance(uncorrect_arrays[array_index], numpy.ndarray):
                self.draw_quantum_state(uncorrect_arrays[array_index], self.disp_Width/4 + (array_index+1)* self.disp_Width/8, self.disp_Height/2)
            else:
                for subarray_index in range(len(uncorrect_arrays[array_index])):
                        self.draw_quantum_state(uncorrect_arrays[array_index][subarray_index].state, self.disp_Width/4 + (array_index+1)* self.disp_Width/8, self.disp_Height/4 + (subarray_index+1) * self.disp_Height/(2*(1+len(uncorrect_arrays[array_index]))), vertically = False)
        pg.display.update()
    
    def victory_View(self, next_level_button):
        background = pg.Rect(self.disp_Width/2, self.disp_Height/2, self.disp_Width/2, self.disp_Height/2)
        background.center = (self.disp_Width/2, self.disp_Height/2)
        pg.draw.rect(self.display, self.colordict["white"], background)
        pg.draw.rect(self.display, self.colordict["black"], background, 10)
        self.draw_text(self.display, "Level complete", self.colordict["black"], self.fontdict["normal"], self.disp_Width/2, self.disp_Height/2)
        pg.draw.rect(self.display, self.colordict["black"], next_level_button, 10)
        self.draw_text(self.display, "next level", self.colordict["black"], self.fontdict["normal"],next_level_button.centerx, next_level_button.centery)
        pg.display.update()