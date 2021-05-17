import pygame as pg
import qiskit as qs
import ctypes
import Circuit_Logic as cl
import pickle
import math

class levelloader():

    # Availables gates
    Hgate = cl.H_Gate(80, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Xgate = cl.X_Gate(90, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Tgate = cl.T_Gate(100, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Zgate = cl.Z_Gate(110, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Sgate = cl.S_Gate(120, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    CONDgate = cl.Conditional_Gate(130, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    SWAPgate = cl.SWAP_Gate(140, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    base_Gates = [Hgate, Xgate, Tgate, Zgate, Sgate, CONDgate, SWAPgate]
    
    levelfile_text = ["Levels\leveltest_file", "Levels\level1_file", "Levels\level2_file", "Levels\level3_file", "Levels\level4_file", "Levels\level5_file", "Levels\level6_file", "Levels\level7_file", "Levels\level8_file"]

    def load_levels(self):
        Levels = []
        for x in range(len(self.levelfile_text)):
            level = pickle.load(open(self.levelfile_text[x], "rb"))
            Levels.append(level)

        return Levels        

    def save_levels(self, levels):
        for x in range(len(levels)):
            pickled_level = pickle.dump(levels[x], open(self.levelfile_text[x], "wb"))

    def setup_levels(self):
        # test level
        test_level = cl.Level([], self.base_Gates,"goal and tutorial bit", "test level")
        pickled_testlevel = pickle.dump(test_level, open("Levels\leveltest_file", "wb"))

        # level 1
        # Setup goal
        level1_qbit1 = cl.Quantum_Bit()
        level1_qbit2 = cl.Quantum_Bit()
        level1_qbit1.set_state(0, 0, 1, 0)
        level1_qbit2.set_state(1, 0, 0, 0)
        
        level1_goal = "Return the qubit with the opposite value using the x gate"
        #print(f"level1 qbit1 state : {level1_qbit1.state}")

        # Initialize level
        level1_ogfile = cl.Level([level1_qbit1, level1_qbit2], self.base_Gates, level1_goal, "Level 1")

        level1_input1 = cl.Quantum_Bit()
        level1_input2 = cl.Quantum_Bit()
        level1_input1.set_state(1, 0, 0, 0)
        level1_input2.set_state(0, 0, 1, 0)
        level1_track1 = cl.Track(level1_ogfile, 0, [level1_input1, level1_input2])
        level1_track1.input.append(level1_input1)
        level1_ogfile.add_track(level1_track1)
        
        pickled_level1 = pickle.dump(level1_ogfile, open("Levels\level1_file", "wb"))

        # level 2
        # Setup goal
        level2_qbit1 = cl.Quantum_Bit()
        level2_qbit1.set_state(0, 0, -1, 0)
        level2_goaltext = "Turn a value of 1 into negative 1 using the z gate"

        # Initialize level
        level2_ogfile = cl.Level([level2_qbit1], self.base_Gates, level2_goaltext, "Level 2")
        
        level2_input1 = cl.Quantum_Bit()
        level2_input1.set_state(0, 0, 1, 0)
        level2_track1 = cl.Track(level2_ogfile, 0, [level2_input1])
        level2_track1.input.append(level2_input1)
        level2_ogfile.add_track(level2_track1)

        pickled_level2 = pickle.dump(level2_ogfile, open("Levels\level2_file", "wb"))

        # level 3
        # Setup goal
        level3_qbit1 = cl.Quantum_Bit()
        level3_qbit1.set_state(0, (1/math.sqrt(2)), 0, (1/math.sqrt(2)))
        level3_goaltext = "Create a superposition using the H gate"

        # Initialize level
        level3_ogfile = cl.Level([level3_qbit1], self.base_Gates, level3_goaltext, "Level 3")

        level3_input1 = cl.Quantum_Bit()
        level3_input1.set_state(1, 0, 0, 0)
        level3_track1 = cl.Track(level3_ogfile, 0, [level3_input1])
        level3_track1.input.append(level3_input1)
        level3_ogfile.add_track(level3_track1)

        pickled_level3 = pickle.dump(level3_ogfile, open("Levels\level3_file", "wb"))

        # level 4
        # Setup goal
        level4_qbit1 = cl.Quantum_Bit()
        level4_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level4_goaltext = "Using a qubit already in superposition, create a circuit that always returns 0"

        # Initialize level
        level4_ogfile = cl.Level([level4_qbit1], self.base_Gates, level4_goaltext, "Level 4")
        
        level4_input1 = cl.Quantum_Bit()
        level4_input1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level4_track1 = cl.Track(level4_ogfile, 0, [level4_input1])
        level4_track1.input.append(level4_input1)
        level4_ogfile.add_track(level4_track1)

        pickled_level4 = pickle.dump(level4_ogfile, open("Levels\level4_file", "wb"))

        # level 5
        # Setup goal
        level5_qbit1 = cl.Quantum_Bit()
        level5_qbit1.set_state(1, 0, 0, 0)
        level5_qbit2 = cl.Quantum_Bit()
        level5_qbit2.set_state(1, 0, 0, 0)
        level5_goaltext = ""

        # Initialize level
        level5_ogfile = cl.Level([level5_qbit1, level5_qbit2], self.base_Gates, level5_goaltext, "Level 5")
        
        level5_input1 = cl.Quantum_Bit()
        level5_input1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level5_track1 = cl.Track(level5_ogfile, 0, [level5_input1])
        level5_track1.input.append(level5_input1)
        level5_ogfile.add_track(level5_track1)
        level5_input2 = cl.Quantum_Bit()
        level5_input2.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level5_track2 = cl.Track(level5_ogfile, 0, [level5_input2])
        level5_track2.input.append(level5_input2)
        level5_ogfile.add_track(level5_track2)

        pickled_level5 = pickle.dump(level5_ogfile, open("Levels\level5_file", "wb"))

        # level 6
        # Setup goal
        level6_qbit1 = cl.Quantum_Bit()
        level6_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level6_qbit2 = cl.Quantum_Bit()
        level6_qbit2.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level6_goaltext = "Create a circuit that has equal vectors in 4 directions"

        # Initialize level
        level6_ogfile = cl.Level([level6_qbit1, level6_qbit2], self.base_Gates, level6_goaltext, "Level 6")
        
        level6_input1 = cl.Quantum_Bit()
        level6_input1.set_state(1, 0, 0, 0)
        level6_track1 = cl.Track(level6_ogfile, 0, [level6_input1])
        level6_track1.input.append(level6_input1)
        level6_ogfile.add_track(level6_track1)
        level6_input2 = cl.Quantum_Bit()
        level6_input2.set_state(1, 0, 0, 0)
        level6_track2 = cl.Track(level6_ogfile, 0, [level6_input2])
        level6_track2.input.append(level6_input2)
        level6_ogfile.add_track(level6_track2)

        pickled_level6 = pickle.dump(level6_ogfile, open("Levels\level6_file", "wb"))
        
        # level 7
        # Setup goal
        level7_qbit1 = cl.Quantum_Bit()
        level7_qbit1.set_state(0, 1, 0, 0)
        level7_qbit2 = cl.Quantum_Bit()
        level7_qbit2.set_state(1, 0, 0, 0)
        level7_goaltext = "Exchange the value of two qubits using the SWAP gate"

        # Initialize level
        level7_ogfile = cl.Level([level7_qbit1, level7_qbit2], self.base_Gates, level7_goaltext, "Level 7")
        
        level7_input1 = cl.Quantum_Bit()
        level7_input1.set_state(1, 0, 0, 0)
        level7_track1 = cl.Track(level7_ogfile, 0, [level7_input1])
        level7_track1.input.append(level7_input1)
        level7_ogfile.add_track(level7_track1)
        level7_input2 = cl.Quantum_Bit()
        level7_input2.set_state(1, 0, 0, 0)
        level7_track2 = cl.Track(level7_ogfile, 0, [level7_input2])
        level7_track2.input.append(level7_input2)
        level7_ogfile.add_track(level7_track2)

        pickled_level7 = pickle.dump(level7_ogfile, open("Levels\level7_file", "wb"))

        # level 8
        # Setup goal
        level8_qbit1 = cl.Quantum_Bit()
        level8_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level8_qbit2 = cl.Quantum_Bit()
        level8_qbit2.set_state(0, 0, 1, 0)
        level8_goaltext = "Circuit output : [0.70710678+0.j, 0.70710678+0.j, 0.+0.j, 0.+0.j]"

        # Initialize level
        level8_ogfile = cl.Level([level8_qbit1, level8_qbit2], self.base_Gates, level8_goaltext, "Level 8")
        
        level8_input1 = cl.Quantum_Bit()
        level8_input1.set_state(1, 0, 0, 0)
        level8_track1 = cl.Track(level8_ogfile, 0, [level8_input1])
        level8_track1.input.append(level8_input1)
        level8_ogfile.add_track(level8_track1)
        level8_input2 = cl.Quantum_Bit()
        level8_input2.set_state(1, 0, 0, 0)
        level8_track2 = cl.Track(level8_ogfile, 0, [level8_input2])
        level8_track2.input.append(level8_input2)
        level8_ogfile.add_track(level8_track2)

        pickled_level8 = pickle.dump(level8_ogfile, open("Levels\level8_file", "wb"))
