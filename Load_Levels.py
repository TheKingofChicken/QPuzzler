import pygame as pg
import ctypes
import Circuit_Logic as cl
import pickle

class levelloader():

    base_Gates = [cl.H_Gate(80, None, None, None, rectangle = pg.Rect(0, 0, 100, 100)), cl.X_Gate(100, None, None, None, rectangle = pg.Rect(0, 0, 100, 100)), cl.T_Gate(120,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.Z_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.S_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.Conditional_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100)), cl.SWAP_Gate(None,None,None,None, rectangle = pg.Rect(0, 0, 100, 100))]
    levelfile_text = ["Levels\leveltest_file", "Levels\level1_file", "Levels\level2_file", "Levels\level3_file", "Levels\level4_file"]
    goaltext_list = ["leveltest goal", "level1 goal", "level2 goal", "level3 goal", "level4 goal"]

    def load_levels(self):
        Levels = []

        test_level = cl.Level([], [], self.base_Gates,"goal and tutorial bit", "test level")
        Levels.append(test_level)
        level1 = pickle.load(open("Levels\level1_file", "rb"))
        Levels.append(level1)
        level2 = pickle.load(open("Levels\level2_file", "rb"))
        Levels.append(level2)
        level3 = pickle.load(open("Levels\level3_file", "rb"))
        Levels.append(level3)
        level4 = pickle.load(open("Levels\level4_file", "rb"))
        Levels.append(level4)

        return Levels        

    def save_levels(self, levels):
        for x in range(len(levels)):
            pickled_level = pickle.dump(levels[x], open(self.levelfile_text[x], "wb"))

    def setup_levels(self):
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
