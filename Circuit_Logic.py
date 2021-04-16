import numpy as np
import qiskit as qs
import cmath
import math
import pygame as pg

class Quantum_Gate():
    def __init__(self, cost, conditional, current_Track, current_Position):
        self.cost = cost
        self.conditional = conditional
        self.current_Track = current_Track
        self.current_Position = current_Position
        self.rectangle = pg.Rect(0, 0, 100, 100)

    def Set_Current_Placement(self, coords):
        self.current_Track = coords[0]
        self.current_position = coords[1]

    def Add_conditional(self, new_conditional):
        self.conditional = new_conditional

class Track(): #class for the track which each qbit moves along
    def __init__(self, input):
        self.input = input
        self.gates = []
        self.total_Cost = 0
        self.rectangle = pg.Rect(430, 0, 1480, 150)
    
    def Add_Gate(self,new_Gate):
        self.gates.append(new_Gate)
        self.total_Cost =+ new_Gate.cost


class Level():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0
        self.tracks = []
    
    def Add_Track(self, track):
        self.tracks.append(track)

    def Run(self):
        #to iterate over the matrix column by column, we place it into a np.array object
        gate_Layers = np.array(self.tracks)
        #construction of the adequate QuantumCircuit object
        q = qs.QuantumRegister(len(self.tracks))
        self.add_register(q)
        for gate_Layer in gate_Layers.transpose():
            for gate in gate_Layer:
                gate.Qiskit_Equivalent_Dispatcher(q)
        
        

class Quantum_Bit:
    def __init__(self):
        self.state = [1,0,0,0]
        self.is_superposed = False
        self.is_entangled = False

    def Set_State(self, zero_Prob, one_Prob, zero_Angle, one_Angle):
        self.state = [zero_Prob,zero_Angle,one_Prob,one_Angle]

    def Update(self, statevector_Coordinates):
       self.state = [np.real(statevector_Coordinates[0]) ** 2 + np.imag(statevector_Coordinates[0]) ** 2, cmath.phase(statevector_Coordinates[0]), np.real(statevector_Coordinates[1]) ** 2 + np.imag(statevector_Coordinates[1]) ** 2, cmath.phase(statevector_Coordinates[1])]
    """the statevector qiskit uses to describe entangled qbits are incomplete, for example: qbit 0 is (50%, 0%) and 1bit 1 is (0%, 50%)
        so far, the way we've found to deal with this is to add the possibilities together, but we still need to check if it would work
        all the time """

    def Get_State(self):
        return self.state

class Conditional_Gate(Quantum_Gate):
    def __init__(self, Control_Qbit):
        self.Control_Qbit = Control_Qbit

#here we start setting up the quantum gate that'll be in the final game
# they're all exactly the same, except for their Qiskit_Equivalent
class SWAP_Gate(Quantum_Gate):
    
    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.swap(self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cswap(self.Conditional.Get_Control_Qbit ,self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class H_Gate(Quantum_Gate):
    
    def __str__(self):
        return "H"

    def __repr__(self):
        return "H"
    
    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.h(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.ch(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class X_Gate(Quantum_Gate):
    
    def __str__(self):
        return "X"

    def __repr__(self):
        return "X"

    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.x(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cnot(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class T_Gate(Quantum_Gate):

    def __str__(self):
        return "T"

    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/4,self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/4, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class Z_Gate(Quantum_Gate):

    def __str__(self):
        return "Z"

    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi,self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class S_Gate(Quantum_Gate):

    def __str__(self):
        return "S"

    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/2,self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def Conditional_Qiskit_Equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/2, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit