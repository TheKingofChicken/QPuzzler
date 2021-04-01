from abc import ABC
from numpy import imag, real
from qiskit import *
import cmath
import math
from qiskit.circuit.quantumregister import Qubit
from qiskit.providers.ibmq.exceptions import IBMQAccountMultipleCredentialsFound

class Quantum_Gate():
    
    def __init__(self, cost, conditionals, current_Track, entity):
        self.cost = cost
        self.conditionals = conditionals
        self.current_Track = current_Track
        self.entity = entity

    def Set_Current_Track(self,new_Track):
        self.current_Track = new_Track

    def Add_conditionals(self, new_conditional, conditional_Slot):
        if conditional_Slot>len(self.conditionals):
            pass
        self.conditionals[conditional_Slot] = new_conditional

    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        Qiskit_Equivalent(self, Quantum_Circuit)# YES IT'S DEFINED WHAT DO YOU FUCKIN MEAN

    def Qiskit_Equivalent(self, quantum_Circuit):
        quantum_Circuit.id(self.current_Track)

class Track(Qubit): #class for the track which each qbit moves along
    def __init__(self, input):
        self.input = input
        self.gates = []
        self.total_Cost = 0
    
    def Add_Gate(self,new_Gate, position):
        self.gates.insert(new_Gate, position)
        self.total_Cost =+ new_Gate.cost
    
    def Get_Gates(self):
        return self.gates

class Level(QuantumCircuit):
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0
        self.tracks = []
        for input in inputs:
            self.tracks.append(Track(input))

    def Add_Track(self):
        self.inputs.append(Track(Quantum_Bit))

    def Run(self):
        gates = []
        longest_Length = 0
        #pulls and stores all the gates, as well as finds the longest one
        for track_Gates in self.tracks:
            gates.append(track_Gates.get_Gates())
            if len(track_Gates.get_Gates())> longest_Length:
                longest_Length = len(track_Gates.get_Gates())
        """ this parts only serves to make the quantum gate array a rectangle, a Quantum_Gate object's quiskit equivalent is an 
        identity gate, which keeps the same qbit"""
        for track_Gates in self.tracks:
            for x in range(longest_Length - len(track_Gates.get_Gates())):
                track_Gates.Add_Gate(Quantum_Gate,len(track_Gates)-1)
        #construction of the adequate QuantumCircuit object
        q = QuantumRegister(len(self.tracks))
        self.add_register(q)
        for track_Position in range(len(self.tracks)):
            for 

class Quantum_Bit:
    def __init__(self):
        self.state = [1,0,0,0]
        self.is_superposed = False
        self.is_entangled = False

    def Set_State(self, zero_Prob, one_Prob, zero_Angle, one_Angle):
        self.state = [zero_Prob,zero_Angle,one_Prob,one_Angle]

    def Update(self, statevector_Coordinates):
       self.state = [real(statevector_Coordinates[0]) ** 2 + imag(statevector_Coordinates[0]) ** 2, cmath.phase(statevector_Coordinates[0]), real(statevector_Coordinates[1]) ** 2 + imag(statevector_Coordinates[1]) ** 2, cmath.phase(statevector_Coordinates[1])]
    """the statevector qiskit uses to describe entangled qbits are incomplete, for example: qbit 0 is (50%, 0%) and 1bit 1 is (0%, 50%)
        so far, the way we've found to deal with this is to add the possibilities together, but we still need to check if it would work
        all the time """

    def Get_State(self):
        return self.state

class Conditional_Gate(Quantum_Gate):
    def __init__(self, Control_Qbit):
        self.Control_Qbit = Control_Qbit

    def Get_Control_Qbit(self):
        return self.Control_Qbit

    def Set_Control_Qbit(self, new_Control_Qbit):
        self.Control_Qbit = new_Control_Qbit

#here we start setting up the quantum gate that'll be in the final game
# they're all exactly the same, except for their Qiskit_Equivalent
class SWAP_Gate(Quantum_Gate):
    def __init__(self, cost, conditionals, current_Track, target_Track, entity):
        self.cost = cost
        self.conditionals = conditionals
        self.current_Track = current_Track
        self.target_Track = target_Track
        self.entity = entity
    
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