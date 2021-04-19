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

    def set_current_placement(self, coords):
        self.current_Track = coords[0]
        self.current_position = coords[1]

    def add_conditional(self, new_conditional):
        self.conditional = new_conditional

class Track(): #class for the track which each qbit moves along
    def __init__(self, input):
        self.input = input
        self.gates = []
        self.total_Cost = 0
        self.rectangle = pg.Rect(430, 0, 1480, 150)
    
    def move_gate(self, pos, new_gate):
        new_gate.current_Track.gates.insert(new_gate.current_Track.gates.index(new_gate), I_Gate(0, 0, self, 0))
        new_gate.current_Track.gates.pop(new_gate.current_Track.gates.index(new_gate))
        if pos < len(self.gates):
            if isinstance(self.gates[pos], I_Gate):
                self.gates.pop(pos)
        self.gates.insert(pos, new_gate)
        new_gate.current_Track = self
        new_gate.current_Position = pos
        

class Level():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0
        self.tracks = []
    
    def add_track(self, track):
        self.tracks.append(track)

    def run(self):
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
        self.state = [1, 0, 0, 0]
        self.is_superposed = False
        self.is_entangled = False

    def set_state(self, zero_Prob, one_Prob, zero_Angle, one_Angle):
        self.state = [zero_Prob, zero_Angle, one_Prob, one_Angle]

    def update(self, statevector_Coordinates):
       self.state = [np.real(statevector_Coordinates[0]) ** 2 + np.imag(statevector_Coordinates[0]) ** 2, cmath.phase(statevector_Coordinates[0]), np.real(statevector_Coordinates[1]) ** 2 + np.imag(statevector_Coordinates[1]) ** 2, cmath.phase(statevector_Coordinates[1])]
    """the statevector qiskit uses to describe entangled qbits are incomplete, for example: qbit 0 is (50%, 0%) and 1bit 1 is (0%, 50%)
        so far, the way we've found to deal with this is to add the possibilities together, but we still need to check if it would work
        all the time """

    def get_state(self):
        return self.state

class Conditional_Gate(Quantum_Gate):
    def __init__(self, Control_Qbit):
        self.Control_Qbit = Control_Qbit

# here we start setting up the quantum gate that'll be in the final game
# they're all exactly the same, except for their Qiskit_Equivalent
class SWAP_Gate(Quantum_Gate):
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.swap(self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cswap(self.Conditional.Get_Control_Qbit , self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class H_Gate(Quantum_Gate):
    
    def __str__(self):
        return "H"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.h(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.ch(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class X_Gate(Quantum_Gate):
    
    def __str__(self):
        return "X"

    def __repr__(self):
        return self.__str__()

    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.x(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cnot(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class T_Gate(Quantum_Gate):

    def __str__(self):
        return "T"

    def __repr__(self):
        return self.__str__()

    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/4, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/4, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class Z_Gate(Quantum_Gate):

    def __str__(self):
        return "Z"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit

class S_Gate(Quantum_Gate):

    def __str__(self):
        return "S"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/2, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/2, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
class I_Gate(Quantum_Gate):
    
    def __str__(self):
        return "I"
    
    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.id(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
