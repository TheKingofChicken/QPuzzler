import pygame as pg
import Circuit_Logic as cl
import pickle
import math
from numpy import array, kron

class levelloader():

    # Availables gates
    Hgate = cl.H_Gate(25, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Xgate = cl.X_Gate(25, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Tgate = cl.T_Gate(10, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Zgate = cl.Z_Gate(35, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    Sgate = cl.S_Gate(20, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    CONDgate = cl.Conditional_Gate(30, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))
    SWAPgate = cl.SWAP_Gate(70, None, None, None, rectangle = pg.Rect(0, 0, 100, 100))

    base_Gates = [Hgate, Xgate, Tgate, Zgate, Sgate, CONDgate, SWAPgate]
    
    levelfile_text = ["Levels\level1_file", "Levels\level2_file", "Levels\level3_file", "Levels\level4_file", "Levels\level5_file", "Levels\level6_file", "Levels\level7_file", "Levels\level8_file"]

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
        # Niveau test
        #test_level = cl.Level([], self.base_Gates,"tutoriel", "test")
        #pickled_testlevel = pickle.dump(test_level, open("Levels\leveltest_file", "wb"))

        # Niveau 1
        # Initialisation du but
        level1_qbit1 = cl.Quantum_Bit()
        level1_qbit2 = cl.Quantum_Bit()
        level1_qbit1.set_state(0, 0, 1, 0)
        level1_qbit2.set_state(1, 0, 0, 0)
        
        level1_goal = "Creez un qubit avec des probilites de 0 et 1 probabilities inversees"
        #print(f"level1 qbit1 state : {level1_qbit1.state}")

        # Initialize level
        level1_ogfile = cl.Level([level1_qbit1.state, level1_qbit2.state], self.base_Gates[0:2], level1_goal, "Niveau 1")

        level1_input1 = cl.Quantum_Bit()
        level1_input2 = cl.Quantum_Bit()
        level1_input1.set_state(1, 0, 0, 0)
        level1_input2.set_state(0, 0, 1, 0)
        level1_track1 = cl.Track(level1_ogfile, 0, [level1_input1, level1_input2], deletable = False)
        level1_ogfile.add_track(level1_track1)
        
        pickled_level1 = pickle.dump(level1_ogfile, open("Levels\level1_file", "wb"))

        
        # level 2
        # Setup goal
        level2_outputs = [cl.Quantum_Bit()]
        for x in range(2):
            level2_outputs.append(cl.Quantum_Bit())
        output_states = [(0,0,-1,0),(0,0,0,-1),(0,0,-1/math.sqrt(2),1/math.sqrt(2))]
        outputs = []
        for qubit, state in zip(level2_outputs, output_states):
            qubit.set_state(state)
            outputs.append(qubit.state)
        level2_goaltext = "Appliquez une rotation a la probabilite 1 de 180 degrees"

        # Initialize level
        level2_ogfile = cl.Level(outputs, self.base_Gates[2:5], level2_goaltext, "Niveau 2")
        
        level2_inputs = [cl.Quantum_Bit()]
        for x in range(2):
            level2_inputs.append(cl.Quantum_Bit())
        input_states = [(0,0,1,0),(0,0,0,1),(0,0,1/math.sqrt(2),-1/math.sqrt(2))]
        for qubit, state in zip(level2_inputs, input_states):
            qubit.set_state(state)
        level2_track1 = cl.Track(level2_ogfile, 0, level2_inputs, deletable = False)
        level2_ogfile.add_track(level2_track1)

        pickled_level2 = pickle.dump(level2_ogfile, open("Levels\level2_file", "wb"))

        # Niveau 3
        # Initialisation du but
        level3_output = []
        num = 1/math.sqrt(2)
        for x in range(5):
            level3_output.append(((cl.Quantum_Bit()),(cl.Quantum_Bit())))
        output_states = [((1,0,0,0),(1,0,0,0)),
                         ((0,0,num,num),(0,0,1,0)),
                         ((1,0,0,0),(1,0,0,0)),
                         ((1,0,0,0),(1,0,0,0)),
                         ((0,0,num,num),(0,0,1,0))]
        for qubit_pair, output_pair in zip(level3_output, output_states):
            for qubit, output in zip(qubit_pair, output_pair):
                qubit.set_state(output)
        output = []
        for output_pair in level3_output:
            output.append(kron(output_pair[1].state,output_pair[0].state))
        level3_goaltext = "mettez le qubit 1 en superposition si le qbit 2 est un"
        
        # Initialise niveau
        level3_ogfile = cl.Level(output, [self.base_Gates[0],self.base_Gates[1],self.base_Gates[5]], level3_goaltext, "Niveau 3")

        level3_input = []
        for x in range(5):
            level3_input.append(((cl.Quantum_Bit()),(cl.Quantum_Bit())))
        input_states = [((1,0,0,0),(1,0,0,0)),
                        ((1,0,0,0),(0,0,1,0)),
                        ((1,0,0,0),(1,0,0,0)),
                        ((1,0,0,0),(1,0,0,0)),
                        ((1,0,0,0),(0,0,1,0))]
        for qubit_pair, input_pair in zip(level3_input, input_states):
            for qubit, input in zip(qubit_pair, input_pair):
                qubit.set_state(input)
        level3_track1 = cl.Track(level3_ogfile, 0, input = [])
        level3_track2 = cl.Track(level3_ogfile, 1, input = [])
        for qubit_pair in level3_input:
            level3_track1.input.append(qubit_pair[0])
            level3_track2.input.append(qubit_pair[1])
        level3_ogfile.add_track(level3_track1)
        level3_ogfile.add_track(level3_track2)
        pickled_level3 = pickle.dump(level3_ogfile, open("Levels\level3_file", "wb"))

        # Niveau 4
        # Initialisation du but
        level4_qbit1 = cl.Quantum_Bit()
        level4_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level4_goaltext = "Avec unn qubit deja en superposition, creez un circuit qui donne toujours 0"

        # Initialise niveau
        level4_ogfile = cl.Level([level4_qbit1], self.base_Gates, level4_goaltext, "Niveau 4")
        
        level4_input1 = cl.Quantum_Bit()
        level4_input1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level4_track1 = cl.Track(level4_ogfile, 0, [level4_input1])
        level4_track1.input.append(level4_input1)
        level4_ogfile.add_track(level4_track1)

        pickled_level4 = pickle.dump(level4_ogfile, open("Levels\level4_file", "wb"))

        # Niveau 5
        # Initialisation du but
        level5_qbit1 = cl.Quantum_Bit()
        level5_qbit1.set_state(1, 0, 0, 0)
        level5_qbit2 = cl.Quantum_Bit()
        level5_qbit2.set_state(1, 0, 0, 0)
        level5_goaltext = ""

        # Initialise niveau
        level5_ogfile = cl.Level([level5_qbit1, level5_qbit2], self.base_Gates, level5_goaltext, "Niveau 5")
        
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

        # Niveau 6
        # Initialisation du but
        level6_qbit1 = cl.Quantum_Bit()
        level6_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level6_qbit2 = cl.Quantum_Bit()
        level6_qbit2.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level6_goaltext = ""

        # Initialise niveau
        level6_ogfile = cl.Level([level6_qbit1, level6_qbit2], self.base_Gates, level6_goaltext, "Niveau 6")
        
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
        
        # Niveau 7
        # Initialisation du but
        level7_qbit1 = cl.Quantum_Bit()
        level7_qbit1.set_state(0, 1, 0, 0)
        level7_qbit2 = cl.Quantum_Bit()
        level7_qbit2.set_state(1, 0, 0, 0)
        level7_goaltext = "Echangez la valeur des deux qubits"

        # Initialise niveau
        level7_ogfile = cl.Level([level7_qbit1, level7_qbit2], self.base_Gates, level7_goaltext, "Niveau 7")
        
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

        # Niveau 8
        # Initialisation du but
        level8_qbit1 = cl.Quantum_Bit()
        level8_qbit1.set_state((1/math.sqrt(2)), 0, (1/math.sqrt(2)), 0)
        level8_qbit2 = cl.Quantum_Bit()
        level8_qbit2.set_state(0, 0, 1, 0)
        level8_goaltext = "Output du circuit : [0.70710678+0.j, 0.70710678+0.j, 0.+0.j, 0.+0.j]"

        # Initialise niveau
        level8_ogfile = cl.Level([level8_qbit1, level8_qbit2], self.base_Gates, level8_goaltext, "Niveau 8")
        
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
