from abc import ABC
from qiskit import *
import math
from qiskit.circuit.quantumregister import Qubit

class Entity:
    def __init__(self, height, width, sprite, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.height = height
        self.width = width
        self.sprite = sprite

class Quantum_Gate(ABC):
    
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

class Track(Qubit):
    def __init__(self, input):
        self.input = input
        self.gates = []
        self.total_Cost = 0
    
    def Add_Gate(self,new_Gate, position):
        self.gates.insert(new_Gate, position)
        self.total_Cost =+ new_Gate.cost

class Level(QuantumCircuit):
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0

    def Add_Track(self):
        self.inputs.append(Track(Quantum_Bit))

class Quantum_Bit:
    def __init__(self):
        self.state = [1,0,0,0]

    def set_State(self, zero_Prob, one_Prob, zero_Angle, one_Angle):
        self.state = [zero_Prob,zero_Angle,one_Prob,one_Angle]

    def Update(self, statevector):
        self.state = statevector #definitely not the final version, Qiskit wont give statevectors in a way thats easily convertible to the qbit object

    def Get_State(self):
        return self.state

class Conditional_Gate(Quantum_Gate):
    def __init__(self, Control_Qbit):
        self.Control_Qbit = Control_Qbit

    def Get_Control_Qbit(self):
        return self.Control_Qbit

    def Set_Control_Qbit(self, new_Control_Qbit):
        self.Control_Qbit = new_Control_Qbit

#here we start setting up the quantum gate that<ll be in the final game
class SWAP_Gate(Quantum_Gate):
    def __init__(self, cost, conditionals, current_Track, target_Track, entity):
        self.cost = cost
        self.conditionals = conditionals
        self.current_Track = current_Track
        self.target_Track = target_Track
        self.entity = entity
    
    def Qiskit_Equivalent_Dispatcher(self, Quantum_Circuit):
        if self.Conditional is None:
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
        if self.Conditional is None:
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
        if self.Conditional is None:
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
        if self.Conditional is None:
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
        if self.Conditional is None:
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
        if self.Conditional is None:
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