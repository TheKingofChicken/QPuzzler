import pygame as pg
import ctypes
import Circuit_Logic as cl

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
        for x in range(len(levels)):
            if level_starters[x] is chosen_level:
                self.draw_text(self.display, levels[x].name, self.colordict["red"], self.fontdict["normal"], self.disp_Width/5 + 240*x, self.disp_Height/4)
            else: self.draw_text(self.display, levels[x].name, self.colordict["black"], self.fontdict["normal"], self.disp_Width/5 + 240*x, self.disp_Height/4)
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
    
    def help_screen_view(self, help_Buttons):
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
        pg.display.update()
    
    def draw_gate(self, level, gate, held_rectangle):
        self.draw_text(self.display,str(gate),self.colordict["black"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
        if isinstance(gate, cl.I_Gate):
            pass
        elif isinstance(gate,cl.Conditional_Gate):
            pg.draw.rect(self.display, self.colordict["grey"], gate.rectangle, 10)
            self.draw_text(self.display, str(gate), self.colordict["grey"], self.fontdict["normal"], gate.rectangle.centerx, gate.rectangle.centery)
            if gate.current_Track:
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
    
    def level_view(self, level, held_rectangle):
        
        self.fps_Limiter.tick(60)
        
        first_layer_elements = []
    
        self.display.fill(self.colordict["white"])
    
        pg.draw.rect(self.display, self.colordict["white"], pg.Rect(10, 10, 400, self.disp_Height-240))
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(10, 10, 400, self.disp_Height-240), 10)
    
        pg.draw.rect(self.display, self.colordict["white"], pg.Rect(10, self.disp_Height-210, self.disp_Width-20, 200))
        pg.draw.rect(self.display, self.colordict["black"], pg.Rect(10, self.disp_Height-210, self.disp_Width-20, 200), 10)
        self.draw_text(self.display, level.goal_text, self.colordict["black"], self.fontdict["normal"], 200, 35)    
    
        pg.draw.rect(self.display, self.colordict["grey"], pg.Rect(430, 10, 80, 50), 10)
        pg.draw.line(self.display, self.colordict["grey"],(470, 20),(470,50), 10)
        pg.draw.line(self.display, self.colordict["grey"],(455, 35),(485,35), 10)
        
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